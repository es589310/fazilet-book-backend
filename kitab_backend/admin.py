from django.contrib import admin
from django.contrib.admin import AdminSite
from django.conf import settings

# Admin panel konfiqurasiyası
admin.site.site_header = getattr(settings, 'ADMIN_SITE_HEADER', '📚 Kitab Satış Sistemi')
admin.site.site_title = getattr(settings, 'ADMIN_SITE_TITLE', 'Kitab Satış Admin')
admin.site.index_title = getattr(settings, 'ADMIN_INDEX_TITLE', 'İdarəetmə Paneli')

# Admin panel stilini yaxşılaşdır
class KitabAdminSite(AdminSite):
    site_header = getattr(settings, 'ADMIN_SITE_HEADER', '📚 Kitab Satış Sistemi')
    site_title = getattr(settings, 'ADMIN_SITE_TITLE', 'Kitab Satış Admin')
    index_title = getattr(settings, 'ADMIN_INDEX_TITLE', 'İdarəetmə Paneli')
    site_url = '/'
    
    def get_app_list(self, request):
        """
        Admin panelində app-lərin sırasını və görünüşünü yaxşılaşdırır
        """
        app_list = super().get_app_list(request)
        
        # App-lərin sırasını təyin et
        app_order = {
            'books': 1,      # Kitablar
            'orders': 2,      # Sifarişlər
            'users': 3,       # İstifadəçilər
            'contact': 4,     # Əlaqə
        }
        
        # App-ləri sırala
        for app in app_list:
            app['admin_order'] = app_order.get(app['app_label'], 999)
        
        app_list.sort(key=lambda x: x['admin_order'])
        
        return app_list

# Admin site instance yarat
kitab_admin_site = KitabAdminSite(name='kitab_admin')

# Mövcud admin site-i yenilə
admin.site.site_header = kitab_admin_site.site_header
admin.site.site_title = kitab_admin_site.site_title
admin.site.index_title = kitab_admin_site.index_title

# Custom CSS əlavə et
class Media:
    css = {
        'all': ('admin/css/custom_admin.css',)
    } 