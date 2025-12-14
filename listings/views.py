from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Q, Max
from django.core.mail import send_mail
from django.conf import settings
from accounts.models import User
from .models import Listing, Category, ListingImage, ListingReport
from .category_fields import get_category_fields
import logging

logger = logging.getLogger(__name__)


def home(request):
    """Homepage with featured and recent listings"""
    logger.info(f"Home page accessed by user: {request.user if request.user.is_authenticated else 'Anonymous'}")
    # Get user's city from location field
    user_city = None
    if request.user.is_authenticated and request.user.location:
        user_city = request.user.location
    
    # Featured listings - prioritize user's city if logged in
    featured_listings = Listing.objects.filter(
        status='active',
        is_featured=True
    ).select_related('seller', 'category', 'seller__company')
    if user_city:
        # Show listings from user's city first, then others
        city_featured = featured_listings.filter(city__icontains=user_city)[:4]
        other_featured = featured_listings.exclude(city__icontains=user_city)[:2]
        featured_listings = list(city_featured) + list(other_featured)
    else:
        featured_listings = featured_listings[:6]
    
    # Recent listings - prioritize user's city if logged in
    recent_listings = Listing.objects.filter(status='active').select_related('seller', 'category', 'seller__company')
    if user_city:
        # Show listings from user's city first
        city_recent = recent_listings.filter(city__icontains=user_city)[:8]
        other_recent = recent_listings.exclude(city__icontains=user_city)[:4]
        recent_listings = list(city_recent) + list(other_recent)
    else:
        recent_listings = recent_listings[:12]
    
    # Show only top-level active categories (no subcategories)
    from django.db.models import Case, When, Value, IntegerField
    
    # Define priority order for important categories
    priority_categories = ['Electronics', 'Vehicles', 'Real Estate', 'Rent', 'Furniture', 
                          'Home Appliances', 'Cars', 'Bikes', 'Apartments']
    
    # Create ordering: priority categories first, then alphabetical
    when_clauses = [When(name=cat, then=Value(i)) for i, cat in enumerate(priority_categories)]
    categories = Category.objects.filter(is_active=True, parent__isnull=True).annotate(
        priority=Case(
            *when_clauses,
            default=Value(999),
            output_field=IntegerField()
        )
    ).order_by('priority', 'name')
    
    context = {
        'featured_listings': featured_listings,
        'recent_listings': recent_listings,
        'categories': categories,
        'user_city': user_city,
    }
    return render(request, 'listings/home.html', context)


def listing_list(request):
    """List all active listings with search and filters"""
    listings = Listing.objects.filter(status='active').select_related('seller', 'category', 'seller__company')
    
    # Get user's city for smart filtering
    user_city = None
    if request.user.is_authenticated and request.user.location:
        user_city = request.user.location
    
    # Search
    query = request.GET.get('q')
    if query:
        listings = listings.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )
    
    # Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        listings = listings.filter(category__slug=category_slug)
    
    # Price filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        listings = listings.filter(price__gte=min_price)
    if max_price:
        listings = listings.filter(price__lte=max_price)
    
    # City filter - default to user's city if not specified
    city_filter = request.GET.get('city')
    if city_filter:
        listings = listings.filter(city__icontains=city_filter)
    elif user_city and not request.GET.get('show_all'):
        # By default, show listings from user's city
        listings = listings.filter(city__icontains=user_city)
    
    # Location/Area filter (within city)
    location = request.GET.get('location')
    if location:
        listings = listings.filter(
            Q(location__icontains=location)
        )
    
    # Condition filter
    condition = request.GET.get('condition')
    if condition:
        listings = listings.filter(condition=condition)
    
    # Sorting - prioritize user's city in default sort
    sort = request.GET.get('sort', '-created_at')
    if user_city and sort == '-created_at' and not city_filter:
        # For default sort, show user's city first
        from django.db.models import Case, When, Value, IntegerField
        listings = listings.annotate(
            is_user_city=Case(
                When(city__icontains=user_city, then=Value(1)),
                default=Value(0),
                output_field=IntegerField()
            )
        ).order_by('-is_user_city', sort)
    else:
        listings = listings.order_by(sort)
    
    categories = Category.objects.filter(parent=None, is_active=True)
    
    context = {
        'listings': listings,
        'categories': categories,
        'user_city': user_city,
        'showing_city_only': bool(user_city and not city_filter and not request.GET.get('show_all')),
    }
    return render(request, 'listings/listing_list.html', context)


def listing_detail(request, slug):
    """Display single listing detail"""
    listing = get_object_or_404(Listing, slug=slug)
    
    # Increment view count
    listing.increment_views()
    
    # Related listings
    related_listings = Listing.objects.filter(
        category=listing.category,
        status='active'
    ).exclude(id=listing.id)[:4]
    
    context = {
        'listing': listing,
        'related_listings': related_listings,
    }
    return render(request, 'listings/listing_detail.html', context)


def category_listings(request, slug):
    """Display listings in a specific category"""
    category = get_object_or_404(Category, slug=slug)
    listings = Listing.objects.filter(category=category, status='active').select_related('seller', 'category', 'seller__company')
    
    # Get user's city for filtering
    user_city = None
    if request.user.is_authenticated and request.user.location:
        user_city = request.user.location
    
    # Search within category
    query = request.GET.get('q')
    if query:
        listings = listings.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        )
    
    # City filter
    city_filter = request.GET.get('city')
    if city_filter:
        listings = listings.filter(city__icontains=city_filter)
    elif user_city and not request.GET.get('show_all'):
        # By default, show listings from user's city
        listings = listings.filter(city__icontains=user_city)
    
    # Condition filter
    condition = request.GET.get('condition')
    if condition:
        listings = listings.filter(condition=condition)
    
    # Sorting
    sort = request.GET.get('sort', '-created_at')
    if user_city and sort == '-created_at' and not city_filter:
        # For default sort, show user's city first
        from django.db.models import Case, When, Value, IntegerField
        listings = listings.annotate(
            is_user_city=Case(
                When(city__icontains=user_city, then=Value(1)),
                default=Value(0),
                output_field=IntegerField()
            )
        ).order_by('-is_user_city', sort)
    else:
        listings = listings.order_by(sort)
    
    context = {
        'category': category,
        'listings': listings,
        'user_city': user_city,
        'showing_city_only': bool(user_city and not city_filter and not request.GET.get('show_all')),
    }
    return render(request, 'listings/category_listings.html', context)


@login_required
def create_listing(request):
    """Create a new listing"""
    if not request.user.can_create_listing():
        # Add detailed error message for debugging
        logger.error(
            f"User {request.user.email} cannot create listing - "
            f"email_verified: {request.user.email_verified}, "
            f"status: {request.user.status}, "
            f"is_active: {request.user.is_active}"
        )
        
        # Provide clear message based on the issue
        if request.user.status == 'waitlist':
            messages.error(
                request,
                f'You cannot create listings yet. Your company ({request.user.company.domain}) is on the waitlist pending admin approval. You will receive an email once your company is approved.'
            )
        elif not request.user.email_verified:
            messages.error(
                request,
                'Please verify your email address before creating listings. Check your inbox for the verification OTP.'
            )
        elif request.user.status == 'rejected':
            messages.error(
                request,
                f'Your company ({request.user.company.domain}) has been rejected. You cannot create listings.'
            )
        else:
            messages.error(
                request,
                'Your account is not approved to create listings. Please contact support.'
            )
        return redirect('accounts:profile')
    
    if request.method == 'POST':
        # Get category to extract its specific fields
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)
        
        # Build attributes dict from category-specific fields
        attributes = {}
        category_fields = get_category_fields(category.name)
        for field_name in category_fields.keys():
            value = request.POST.get(f'attr_{field_name}')
            if value:
                attributes[field_name] = value
        
        # Create listing
        listing = Listing.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            category_id=category_id,
            seller=request.user,
            price=request.POST.get('price'),
            is_negotiable=request.POST.get('is_negotiable') == 'on',
            condition=request.POST.get('condition'),
            location=request.POST.get('location'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            pincode=request.POST.get('pincode', ''),
            attributes=attributes,  # Save category-specific attributes
        )
        
        # Handle multiple images (max 8)
        images = request.FILES.getlist('images')
        if len(images) > 8:
            messages.warning(request, 'Only the first 8 images were uploaded. Maximum 8 images allowed per listing.')
            images = images[:8]
        
        for idx, image in enumerate(images):
            ListingImage.objects.create(
                listing=listing,
                image=image,
                order=idx
            )
        
        messages.success(request, 'Listing created successfully!')
        return redirect('listings:listing_detail', slug=listing.slug)
    
    # Get all categories - both parent and subcategories
    parent_categories = Category.objects.filter(parent=None, is_active=True).prefetch_related('subcategories')
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'parent_categories': parent_categories,
        'categories': categories,
    }
    return render(request, 'listings/create_listing.html', context)


@login_required
def edit_listing(request, slug):
    """Edit existing listing"""
    listing = get_object_or_404(Listing, slug=slug)
    
    # Check if user is the owner
    if listing.seller != request.user:
        logger.warning(f"User {request.user.email} attempted to edit listing {slug} owned by {listing.seller.email}")
        raise PermissionDenied("You don't have permission to edit this listing.")
    
    if request.method == 'POST':
        listing.title = request.POST.get('title')
        listing.description = request.POST.get('description')
        listing.category_id = request.POST.get('category')
        listing.price = request.POST.get('price')
        listing.is_negotiable = request.POST.get('is_negotiable') == 'on'
        listing.condition = request.POST.get('condition')
        listing.location = request.POST.get('location')
        listing.city = request.POST.get('city')
        listing.state = request.POST.get('state')
        listing.pincode = request.POST.get('pincode', '')
        
        # Handle category-specific attributes
        category = Category.objects.get(id=listing.category_id)
        category_fields = get_category_fields(category.id)
        
        if category_fields:
            attributes = {}
            for field_name in category_fields.keys():
                field_value = request.POST.get(f'attr_{field_name}')
                if field_value:
                    attributes[field_name] = field_value
            listing.attributes = attributes
        
        listing.save()
        
        # Handle image deletions
        deleted_image_ids = request.POST.getlist('delete_images')
        if deleted_image_ids:
            deleted_count = ListingImage.objects.filter(
                id__in=deleted_image_ids,
                listing=listing
            ).delete()[0]
            if deleted_count > 0:
                logger.info(f"User {request.user.email} deleted {deleted_count} images from listing {slug}")
        
        # Handle new image uploads
        new_images = request.FILES.getlist('new_images')
        current_image_count = listing.images.count()
        
        if new_images:
            # Limit to 8 total images
            available_slots = 8 - current_image_count
            if len(new_images) > available_slots:
                messages.warning(request, f'Only {available_slots} images can be added. Maximum 8 images per listing.')
                new_images = new_images[:available_slots]
            
            # Get highest order number
            max_order = listing.images.aggregate(Max('order'))['order__max'] or -1
            
            for idx, image in enumerate(new_images):
                ListingImage.objects.create(
                    listing=listing,
                    image=image,
                    order=max_order + idx + 1
                )
            
            if new_images:
                logger.info(f"User {request.user.email} added {len(new_images)} images to listing {slug}")
                messages.success(request, f'{len(new_images)} image(s) added successfully!')
        
        # Handle image reordering
        image_orders = request.POST.get('image_order')
        if image_orders:
            try:
                order_list = [int(x) for x in image_orders.split(',') if x.strip()]
                for new_order, image_id in enumerate(order_list):
                    ListingImage.objects.filter(
                        id=image_id,
                        listing=listing
                    ).update(order=new_order)
                logger.info(f"User {request.user.email} reordered images for listing {slug}")
            except (ValueError, TypeError) as e:
                logger.error(f"Error reordering images for listing {slug}: {e}")
        
        messages.success(request, 'Listing updated successfully!')
        return redirect('listings:listing_detail', slug=listing.slug)
    
    parent_categories = Category.objects.filter(parent__isnull=True, is_active=True).order_by('order')
    categories = Category.objects.filter(is_active=True)
    context = {
        'listing': listing,
        'parent_categories': parent_categories,
        'categories': categories,
    }
    return render(request, 'listings/edit_listing.html', context)


@login_required
def delete_image(request, image_id):
    """Delete a single listing image (AJAX endpoint)"""
    from django.http import JsonResponse
    
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid method'}, status=405)
    
    try:
        image = get_object_or_404(ListingImage, id=image_id)
        listing = image.listing
        
        # Check if user is the owner
        if listing.seller != request.user:
            logger.warning(f"User {request.user.email} attempted to delete image {image_id} from listing owned by {listing.seller.email}")
            return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
        
        # Prevent deletion if it's the last image (optional - can be removed if you want to allow 0 images)
        if listing.images.count() <= 1:
            return JsonResponse({'success': False, 'error': 'Cannot delete the last image'}, status=400)
        
        image.delete()
        logger.info(f"User {request.user.email} deleted image {image_id} from listing {listing.slug}")
        
        return JsonResponse({
            'success': True,
            'remaining_count': listing.images.count()
        })
    
    except Exception as e:
        logger.error(f"Error deleting image {image_id}: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
def delete_listing(request, slug):
    """Delete listing"""
    listing = get_object_or_404(Listing, slug=slug)
    
    # Check if user is the owner
    if listing.seller != request.user:
        logger.warning(f"User {request.user.email} attempted to delete listing {slug} owned by {listing.seller.email}")
        raise PermissionDenied("You don't have permission to delete this listing.")
    
    if request.method == 'POST':
        listing.status = 'deleted'
        listing.save()
        messages.success(request, 'Listing deleted successfully!')
        return redirect('listings:my_listings')
    
    return render(request, 'listings/delete_listing.html', {'listing': listing})


@login_required
def mark_sold(request, slug):
    """Mark listing as sold"""
    listing = get_object_or_404(Listing, slug=slug)
    
    # Check if user is the owner
    if listing.seller != request.user:
        logger.warning(f"User {request.user.email} attempted to mark listing {slug} as sold, owned by {listing.seller.email}")
        raise PermissionDenied("You don't have permission to modify this listing.")
    
    if request.method == 'POST':
        listing.status = 'sold'
        listing.save()
        logger.info(f"Listing {slug} marked as sold by owner {request.user.email}")
        messages.success(request, 'Listing marked as SOLD! The item has been deactivated.')
        return redirect('listings:listing_detail', slug=slug)
    
    # If not POST, redirect back to listing
    return redirect('listings:listing_detail', slug=slug)


@login_required
def my_listings(request):
    """Display user's own listings"""
    listings = Listing.objects.filter(seller=request.user).exclude(status='deleted').select_related('category').prefetch_related('images')
    
    context = {'listings': listings}
    return render(request, 'listings/my_listings.html', context)


@login_required
def company_listings(request):
    """Display listings from user's company"""
    if not request.user.company:
        messages.warning(request, 'You need to be associated with a company to view company listings.')
        return redirect('listings:listing_list')
    
    listings = Listing.objects.filter(
        seller__company=request.user.company,
        status='active'
    ).exclude(seller=request.user).select_related('seller', 'category', 'seller__company')
    
    context = {
        'listings': listings,
        'company': request.user.company,
    }
    return render(request, 'listings/company_listings.html', context)


from django.http import JsonResponse

def get_category_fields_api(request, category_id):
    """API endpoint to get category-specific fields configuration"""
    try:
        category = Category.objects.get(id=category_id)
        fields = get_category_fields(category.name)
        return JsonResponse({
            'success': True,
            'category_name': category.name,
            'fields': fields
        })
    except Category.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Category not found'
        }, status=404)


@login_required
def report_listing(request, listing_id):
    """Report a listing for inappropriate content"""
    listing = get_object_or_404(Listing, id=listing_id)
    
    # Check if user already reported this listing
    existing_report = ListingReport.objects.filter(
        listing=listing,
        reporter=request.user
    ).first()
    
    if existing_report:
        messages.warning(request, 'You have already reported this listing.')
        return redirect('listings:listing_detail', listing_id=listing.id)
    
    if request.method == 'POST':
        reason = request.POST.get('reason')
        description = request.POST.get('description', '')
        
        if not reason:
            messages.error(request, 'Please select a reason for reporting.')
            return redirect('listings:listing_detail', listing_id=listing.id)
        
        # Create the report
        report = ListingReport.objects.create(
            listing=listing,
            reporter=request.user,
            reason=reason,
            description=description,
            status='pending'
        )
        
        logger.info(f"Listing #{listing.id} reported by {request.user.email} - Reason: {reason}")
        
        # Send email notification to admins
        try:
            admin_users = User.objects.filter(is_staff=True, is_active=True)
            admin_emails = [admin.email for admin in admin_users if admin.email]
            
            if admin_emails:
                report_count = listing.reports.count()
                subject = f'🚨 Listing Reported - {listing.title[:50]}'
                message = f"""
A listing has been reported on CredMarket:

Listing: {listing.title}
Listing URL: {settings.SITE_URL}/listings/{listing.id}/
Reported by: {request.user.email} ({request.user.company.name if request.user.company else 'N/A'})
Reason: {report.get_reason_display()}
Description: {description}

Total Reports for this listing: {report_count}

Review this report in the admin panel:
{settings.SITE_URL}/admin/listings/listingreport/{report.id}/change/

---
CredMarket Admin System
                """
                
                # Send email async to avoid blocking
                import threading
                def _send():
                    try:
                        send_mail(
                            subject,
                            message,
                            settings.DEFAULT_FROM_EMAIL,
                            admin_emails,
                            fail_silently=True,
                            timeout=10,
                        )
                        logger.info(f"Report notification email sent to {len(admin_emails)} admins")
                    except Exception as email_err:
                        logger.error(f"Failed to send report notification email: {email_err}")
                
                threading.Thread(target=_send, daemon=True).start()
        except Exception as e:
            logger.error(f"Failed to prepare report notification: {e}")
        
        messages.success(
            request,
            'Thank you for your report. Our team will review it shortly.'
        )
        return redirect('listings:listing_detail', listing_id=listing.id)
    
    # GET request - show report form
    return render(request, 'listings/report_listing.html', {
        'listing': listing,
        'report_reasons': ListingReport.REPORT_REASONS
    })
