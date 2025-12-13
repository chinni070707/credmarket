from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Count
from django.utils import timezone
from .models import Company
from accounts.models import User


@staff_member_required
def admin_dashboard(request):
    """Custom admin dashboard with stats and quick actions"""
    # Get total stats
    total_users = User.objects.count()
    total_companies = Company.objects.values('domain').distinct().count()
    approved_companies = Company.objects.filter(status='approved').count()
    waitlist_companies = Company.objects.filter(status='waitlist').count()
    rejected_companies = Company.objects.filter(status='rejected').count()
    
    # Get user count by city
    users_by_city = User.objects.values('location').annotate(
        count=Count('id')
    ).filter(location__isnull=False).exclude(location='').order_by('-count')[:10]
    
    # Get recent waitlist companies
    waitlist_list = Company.objects.filter(status='waitlist').order_by('-created_at')[:10]
    
    context = {
        'total_users': total_users,
        'total_companies': total_companies,
        'approved_companies': approved_companies,
        'waitlist_companies': waitlist_companies,
        'rejected_companies': rejected_companies,
        'users_by_city': users_by_city,
        'waitlist_list': waitlist_list,
    }
    
    return render(request, 'companies/admin_dashboard.html', context)


@staff_member_required
def approve_company(request, company_id):
    """Approve a company and update users"""
    company = get_object_or_404(Company, id=company_id)
    
    if company.status != 'approved':
        company.status = 'approved'
        company.approved_by = request.user
        company.approved_at = timezone.now()
        company.save()
        
        messages.success(request, f'{company.name} has been approved! Emails sent to waitlisted users.')
    else:
        messages.info(request, f'{company.name} is already approved.')
    
    return redirect('companies:admin_dashboard')


@staff_member_required
def reject_company(request, company_id):
    """Reject a company"""
    company = get_object_or_404(Company, id=company_id)
    
    company.status = 'rejected'
    company.save()
    
    messages.warning(request, f'{company.name} has been rejected.')
    return redirect('companies:admin_dashboard')


@staff_member_required
def approved_companies_list(request):
    """Show all approved companies"""
    approved_companies = Company.objects.filter(status='approved').order_by('-approved_at')
    
    context = {
        'companies': approved_companies,
        'title': 'Approved Companies'
    }
    
    return render(request, 'companies/companies_list.html', context)


@staff_member_required
def add_company(request):
    """Add a new company directly"""
    if request.method == 'POST':
        name = request.POST.get('name')
        domain = request.POST.get('domain')
        description = request.POST.get('description', '')
        website = request.POST.get('website', '')
        status = request.POST.get('status', 'approved')
        
        if not name or not domain:
            messages.error(request, 'Name and domain are required.')
            return redirect('companies:admin_dashboard')
        
        # Check if domain already exists
        if Company.objects.filter(domain=domain).exists():
            messages.error(request, f'Company with domain {domain} already exists.')
            return redirect('companies:admin_dashboard')
        
        company = Company.objects.create(
            name=name,
            domain=domain,
            description=description,
            website=website,
            status=status,
            added_by=request.user
        )
        
        if status == 'approved':
            company.approved_by = request.user
            company.approved_at = timezone.now()
            company.save()
        
        messages.success(request, f'{name} has been added successfully!')
        return redirect('companies:admin_dashboard')
    
    return redirect('companies:admin_dashboard')


@staff_member_required
def delete_company(request, company_id):
    """Delete a company"""
    if request.method == 'POST':
        company = get_object_or_404(Company, id=company_id)
        company_name = company.name
        
        # Delete the company (this will also affect associated users)
        company.delete()
        
        messages.success(request, f'{company_name} has been removed successfully.')
        return redirect('companies:approved_companies_list')
    
    return redirect('companies:approved_companies_list')
