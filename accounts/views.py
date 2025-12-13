from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
import random
from .models import User, OTPVerification


def signup(request):
    """Handle user signup with email verification"""
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        phone = request.POST.get('phone', '').strip()
        city = request.POST.get('city', '').strip()
        area = request.POST.get('area', '').strip()
        display_name = request.POST.get('display_name', '').strip()
        show_real_name = request.POST.get('show_real_name') == 'on'
        latitude = request.POST.get('latitude', '').strip()
        longitude = request.POST.get('longitude', '').strip()
        
        # Validate city is provided
        if not city:
            messages.error(request, 'City is required.')
            return render(request, 'accounts/signup.html')
        
        # Extract domain from email
        domain = email.split('@')[1] if '@' in email else None
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'accounts/signup.html')
        
        # Check if domain is in whitelist
        from companies.models import Company
        try:
            company = Company.objects.get(domain=domain, status='approved')
            user_status = 'pending'
        except Company.DoesNotExist:
            # Check if domain is already in waitlist
            if Company.objects.filter(domain=domain, status='waitlist').exists():
                user_status = 'waitlist'
                company = Company.objects.get(domain=domain)
            else:
                # Create new waitlist entry
                company = Company.objects.create(
                    domain=domain,
                    name=domain.split('.')[0].title(),
                    status='waitlist'
                )
                user_status = 'waitlist'
        
        # Create user
        username = email.split('@')[0] + str(random.randint(1000, 9999))
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            phone=phone if phone else None,
            location=city,
            area=area if area else '',
            latitude=float(latitude) if latitude else None,
            longitude=float(longitude) if longitude else None,
            display_name=display_name if display_name else '',
            show_real_name=show_real_name,
            company=company,
            status=user_status
        )
        
        # Generate and send OTP for all users (including waitlisted)
        otp_code = str(random.randint(100000, 999999))
        expires_at = timezone.now() + timedelta(minutes=10)
        
        OTPVerification.objects.create(
            user=user,
            otp_code=otp_code,
            expires_at=expires_at
        )
        
        # TODO: Send email with OTP
        # For now, just display it (in development)
        print(f"OTP for {email}: {otp_code}")
        
        # Store user_id in session for OTP verification
        request.session['pending_user_id'] = user.id
        
        # Different messages for waitlist vs approved companies
        if user_status == 'waitlist':
            messages.info(request, f'Your company ({domain}) is being reviewed. Please verify your email to complete registration.')
        else:
            messages.success(request, f'OTP sent to {email}. Please verify to complete registration.')
        
        return redirect('accounts:verify_otp')
    
    return render(request, 'accounts/signup.html')


def waitlist(request):
    """Display waitlist confirmation page"""
    user_id = request.session.get('waitlist_user_id')
    
    if not user_id:
        messages.error(request, 'No waitlist registration found.')
        return redirect('accounts:signup')
    
    try:
        user = User.objects.get(id=user_id)
        company_name = user.company.name if user.company else 'Unknown'
        
        context = {
            'user': user,
            'company_name': company_name,
        }
        return render(request, 'accounts/waitlist.html', context)
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('accounts:signup')


def verify_otp(request):
    """Verify OTP sent to user's email"""
    user_id = request.session.get('pending_user_id')
    
    if not user_id:
        messages.error(request, 'No pending verification found.')
        return redirect('accounts:signup')
    
    if request.method == 'POST':
        otp_code = request.POST.get('otp_code')
        
        try:
            user = User.objects.get(id=user_id)
            otp = OTPVerification.objects.filter(
                user=user,
                otp_code=otp_code,
                is_used=False
            ).latest('created_at')
            
            if otp.is_valid():
                otp.is_used = True
                otp.save()
                
                user.email_verified = True
                if user.status == 'pending':
                    user.status = 'approved'
                user.save()
                
                # Clear session
                del request.session['pending_user_id']
                
                # Handle waitlisted users differently
                if user.status == 'waitlist':
                    # Store user info for waitlist page
                    request.session['waitlist_user_id'] = user.id
                    messages.success(request, 'Email verified! Your account is pending company approval.')
                    return redirect('accounts:waitlist')
                
                # Log approved users in immediately
                login(request, user)
                messages.success(request, 'Email verified successfully! Welcome to CredMarket.')
                return redirect('listings:home')
            else:
                messages.error(request, 'OTP has expired. Please request a new one.')
        except OTPVerification.DoesNotExist:
            messages.error(request, 'Invalid OTP code.')
    
    return render(request, 'accounts/verify_otp.html')


def login_view(request):
    """Handle user login"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            if not user.email_verified:
                messages.error(request, 'Please verify your email first.')
                return redirect('accounts:verify_otp')
            
            if user.status == 'waitlist':
                messages.warning(request, f'Your company ({user.company.domain if user.company else "domain"}) is being reviewed by our team. You\'ll receive an email once approved (usually within 1-2 business days).')
                return render(request, 'accounts/login.html', {'debug': settings.DEBUG})
            
            if user.status == 'suspended':
                messages.error(request, 'Your account has been suspended.')
                return render(request, 'accounts/login.html', {'debug': settings.DEBUG})
            
            login(request, user)
            
            # Redirect admin/superuser to custom admin dashboard
            if user.is_staff or user.is_superuser:
                messages.success(request, f'Welcome back, Admin!')
                return redirect('companies:admin_dashboard')
            
            messages.success(request, f'Welcome back, {user.first_name}!')
            return redirect('listings:home')
        else:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'accounts/login.html', {'debug': settings.DEBUG})


@login_required
def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')


@login_required
def profile(request):
    """Display user profile"""
    return render(request, 'accounts/profile.html', {'user': request.user})


@login_required
def edit_profile(request):
    """Edit user profile"""
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.phone = request.POST.get('phone')
        request.user.bio = request.POST.get('bio')
        request.user.location = request.POST.get('location')
        request.user.area = request.POST.get('area', '')
        request.user.display_name = request.POST.get('display_name', '')
        request.user.show_real_name = request.POST.get('show_real_name') == 'on'
        
        if request.FILES.get('profile_picture'):
            request.user.profile_picture = request.FILES['profile_picture']
        
        request.user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:profile')
    
    return render(request, 'accounts/edit_profile.html')
