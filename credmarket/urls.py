"""
URL configuration for credmarket project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from .health import health_check, readiness_check, liveness_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('listings.urls')),
    path('accounts/', include('accounts.urls')),
    path('messages/', include('messaging.urls')),
    path('companies/', include('companies.urls')),
    
    # Health check endpoints
    path('health/', health_check, name='health_check'),
    path('healthz', health_check, name='healthz'),  # Render default health check
    path('ready/', readiness_check, name='readiness'),
    path('alive/', liveness_check, name='liveness'),
    
    # Static pages
    path('how-it-works/', TemplateView.as_view(template_name='how_it_works.html'), name='how_it_works'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
]

# Customize admin site
admin.site.site_header = 'CredMarket Administration'
admin.site.site_title = 'CredMarket Admin'
admin.site.index_title = 'Welcome to CredMarket Admin Panel'

# Debug toolbar
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error handlers
handler404 = 'credmarket.views.custom_404'
handler500 = 'credmarket.views.custom_500'
handler403 = 'credmarket.views.custom_403'
