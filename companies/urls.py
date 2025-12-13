from django.urls import path
from . import views

app_name = 'companies'

urlpatterns = [
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('approve/<int:company_id>/', views.approve_company, name='approve_company'),
    path('reject/<int:company_id>/', views.reject_company, name='reject_company'),
    path('approved-list/', views.approved_companies_list, name='approved_companies_list'),
    path('add-company/', views.add_company, name='add_company'),
    path('delete/<int:company_id>/', views.delete_company, name='delete_company'),
]
