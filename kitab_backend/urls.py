from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse, HttpResponse
from django.db import connection
import django.utils.timezone
import os

# Admin konfiqurasiyasını import et
from . import admin as admin_config

# Admin panel başlıqlarını dəyişirik
admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE
admin.site.index_title = settings.ADMIN_INDEX_TITLE

# Favicon view
def favicon_view(request):
    """Serve favicon.ico to prevent 404 errors"""
    favicon_path = os.path.join(settings.STATIC_ROOT or settings.STATICFILES_DIRS[0], 'favicon.ico')
    if os.path.exists(favicon_path):
        with open(favicon_path, 'rb') as f:
            return HttpResponse(f.read(), content_type='image/x-icon')
    else:
        # Return empty favicon if file doesn't exist
        return HttpResponse(b'', content_type='image/x-icon')

# Health check view
def health_check(request):
    """Production health check endpoint"""
    return HttpResponse("Django backend is running successfully!", content_type="text/plain")

# Production URL patterns
urlpatterns = [
    path('', health_check, name='root'),  # Root path
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/books/', include('books.urls')),
    path('api/settings/', include('settings.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/contact/', include('contact.urls')),
    path('health/', health_check, name='health_check'),
    path('favicon.ico', favicon_view, name='favicon'),
]

# Static and Media files serving
if settings.DEBUG:
    # Development: Serve static and media files through Django
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # Production: Static files should be served by web server (nginx/apache)
    # Media files can be served by Django or web server
    # Uncomment the line below if you want Django to serve media files in production
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    pass
