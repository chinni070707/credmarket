from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Listing, Category, ListingImage


def home(request):
    """Homepage with featured and recent listings"""
    featured_listings = Listing.objects.filter(
        status='active',
        is_featured=True
    )[:6]
    
    recent_listings = Listing.objects.filter(
        status='active'
    )[:12]
    
    categories = Category.objects.filter(parent=None, is_active=True)
    
    context = {
        'featured_listings': featured_listings,
        'recent_listings': recent_listings,
        'categories': categories,
    }
    return render(request, 'listings/home.html', context)


def listing_list(request):
    """List all active listings with search and filters"""
    listings = Listing.objects.filter(status='active')
    
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
    
    # Location filter
    location = request.GET.get('location')
    if location:
        listings = listings.filter(
            Q(city__icontains=location) |
            Q(location__icontains=location)
        )
    
    # Condition filter
    condition = request.GET.get('condition')
    if condition:
        listings = listings.filter(condition=condition)
    
    # Sorting
    sort = request.GET.get('sort', '-created_at')
    listings = listings.order_by(sort)
    
    categories = Category.objects.filter(parent=None, is_active=True)
    
    context = {
        'listings': listings,
        'categories': categories,
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
    listings = Listing.objects.filter(category=category, status='active')
    
    context = {
        'category': category,
        'listings': listings,
    }
    return render(request, 'listings/category_listings.html', context)


@login_required
def create_listing(request):
    """Create a new listing"""
    if not request.user.can_create_listing():
        messages.error(request, 'You need to be verified to create listings.')
        return redirect('accounts:profile')
    
    if request.method == 'POST':
        listing = Listing.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            category_id=request.POST.get('category'),
            seller=request.user,
            price=request.POST.get('price'),
            is_negotiable=request.POST.get('is_negotiable') == 'on',
            condition=request.POST.get('condition'),
            location=request.POST.get('location'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            pincode=request.POST.get('pincode', ''),
        )
        
        # Handle multiple images
        images = request.FILES.getlist('images')
        for idx, image in enumerate(images):
            ListingImage.objects.create(
                listing=listing,
                image=image,
                order=idx
            )
        
        messages.success(request, 'Listing created successfully!')
        return redirect('listings:listing_detail', slug=listing.slug)
    
    categories = Category.objects.filter(is_active=True)
    context = {'categories': categories}
    return render(request, 'listings/create_listing.html', context)


@login_required
def edit_listing(request, slug):
    """Edit existing listing"""
    listing = get_object_or_404(Listing, slug=slug, seller=request.user)
    
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
        listing.save()
        
        messages.success(request, 'Listing updated successfully!')
        return redirect('listings:listing_detail', slug=listing.slug)
    
    categories = Category.objects.filter(is_active=True)
    context = {
        'listing': listing,
        'categories': categories,
    }
    return render(request, 'listings/edit_listing.html', context)


@login_required
def delete_listing(request, slug):
    """Delete listing"""
    listing = get_object_or_404(Listing, slug=slug, seller=request.user)
    
    if request.method == 'POST':
        listing.status = 'deleted'
        listing.save()
        messages.success(request, 'Listing deleted successfully!')
        return redirect('listings:my_listings')
    
    return render(request, 'listings/delete_listing.html', {'listing': listing})


@login_required
def my_listings(request):
    """Display user's own listings"""
    listings = Listing.objects.filter(seller=request.user).exclude(status='deleted')
    
    context = {'listings': listings}
    return render(request, 'listings/my_listings.html', context)
