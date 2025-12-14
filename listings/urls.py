from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    path('', views.home, name='home'),
    path('listings/', views.listing_list, name='listing_list'),
    path('listings/create/', views.create_listing, name='create_listing'),
    path('listings/<slug:slug>/', views.listing_detail, name='listing_detail'),
    path('listings/<slug:slug>/edit/', views.edit_listing, name='edit_listing'),
    path('listings/<slug:slug>/delete/', views.delete_listing, name='delete_listing'),
    path('listings/<int:listing_id>/report/', views.report_listing, name='report_listing'),
    path('category/<slug:slug>/', views.category_listings, name='category_listings'),
    path('my-listings/', views.my_listings, name='my_listings'),
    path('company-listings/', views.company_listings, name='company_listings'),
    path('api/category-fields/<int:category_id>/', views.get_category_fields_api, name='category_fields_api'),
]
