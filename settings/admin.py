from django.contrib import admin
from .models import SiteSettings, Logo

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'phone', 'email', 'whatsapp_number', 'copyright_year']
    fieldsets = (
        ('Əsas Məlumatlar', {
            'fields': ('site_name', 'site_description')
        }),
        ('Əlaqə Məlumatları', {
            'fields': ('phone', 'email', 'address', 'working_hours', 'whatsapp_number')
        }),
        ('Copyright', {
            'fields': ('copyright_year',)
        }),
        ('Sosial Media', {
            'fields': ('facebook', 'instagram', 'twitter', 'youtube'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Yalnız bir instance ola bilər
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Silməyə icazə vermə
        return False
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('admin/js/admin_icons.js',)


@admin.register(Logo)
class LogoAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'has_navbar_logo', 'has_footer_logo', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['site_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Logo Tənzimləmələri', {
            'fields': ('navbar_logo', 'navbar_logo_imagekit_url', 'footer_logo', 'footer_logo_imagekit_url'),
            'description': 'Navbar və Footer üçün logo-ları yükləyin. ImageKit URL-ləri avtomatik doldurulacaq.'
        }),
        ('Sayt Məlumatları', {
            'fields': ('site_name', 'is_active')
        }),
    )
    
    def has_navbar_logo(self, obj):
        return bool(obj.navbar_logo)
    has_navbar_logo.boolean = True
    has_navbar_logo.short_description = 'Navbar Logo'
    
    def has_footer_logo(self, obj):
        return bool(obj.footer_logo)
    has_footer_logo.boolean = True
    has_footer_logo.short_description = 'Footer Logo'
    
    def has_add_permission(self, request):
        # Yalnız bir tənzimləmə olsun
        return not Logo.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Silməyə icazə vermə
        return False
    
    def save_model(self, request, obj, form, change):
        """Logo yükləndikdə avtomatik olaraq ImageKit-ə yükləyir"""
        super().save_model(request, obj, form, change)
        
        # Navbar logo yüklə
        if 'navbar_logo' in form.changed_data and obj.navbar_logo:
            try:
                from lib.imagekit_utils import imagekit_manager
                IMAGEKIT_AVAILABLE = True
            except ImportError:
                IMAGEKIT_AVAILABLE = False
                print("Warning: lib.imagekit_utils not available, skipping logo upload")
                return
            result = imagekit_manager.upload_image(
                obj.navbar_logo, 
                folder_path='site/navbar',
                filename=f"navbar_logo_{obj.id}"
            )
            if result['success']:
                obj.navbar_logo_imagekit_url = result['url']
                obj.save(update_fields=['navbar_logo_imagekit_url'])
                print(f"✅ Navbar logo ImageKit-ə yükləndi: {result['url']}")
            else:
                print(f"❌ Navbar logo yükləmə xətası: {result.get('error')}")
        
        # Footer logo yüklə
        if 'footer_logo' in form.changed_data and obj.footer_logo:
            try:
                from lib.imagekit_utils import imagekit_manager
                IMAGEKIT_AVAILABLE = True
            except ImportError:
                IMAGEKIT_AVAILABLE = False
                print("Warning: lib.imagekit_utils not available, skipping logo upload")
                return
            result = imagekit_manager.upload_image(
                obj.footer_logo, 
                folder_path='site/footer',
                filename=f"footer_logo_{obj.id}"
            )
            if result['success']:
                obj.footer_logo_imagekit_url = result['url']
                obj.save(update_fields=['footer_logo_imagekit_url'])
                print(f"✅ Footer logo ImageKit-ə yükləndi: {result['url']}")
            else:
                print(f"❌ Footer logo yükləmə xətası: {result.get('error')}")
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('admin/js/admin_icons.js',)
