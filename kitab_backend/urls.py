from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

# Admin panel başlıqlarını dəyişirik
admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE
admin.site.index_title = settings.ADMIN_INDEX_TITLE

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/books/', include('books.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/contact/', include('contact.urls')),
    path('test-imagekit/', TemplateView.as_view(template_name='test_imagekit.html'), name='test-imagekit'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Media files serving in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
