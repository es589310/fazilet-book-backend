from django.contrib import admin
from .models import ContactMessage, SocialMediaLink, SiteSettings

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['sender_name', 'sender_email', 'subject', 'status', 'created_at', 'auto_reply_sent']
    list_filter = ['status', 'auto_reply_sent', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message', 'user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Göndərən məlumatları', {
            'fields': ('user', 'name', 'email'),
            'description': 'Mesaj göndərən şəxsin məlumatları'
        }),
        ('Mesaj məlumatları', {
            'fields': ('subject', 'message', 'status'),
            'description': 'Mesajın əsas məlumatları və statusu'
        }),
        ('Avtomatik cavab', {
            'fields': ('auto_reply_sent', 'auto_reply_date'),
            'description': 'Avtomatik cavab göndərilməsi haqqında məlumat'
        }),
        ('Tarix məlumatları', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
            'description': 'Mesajın yaradılma və yenilənmə tarixləri'
        }),
    )
    
    def sender_name(self, obj):
        return obj.sender_name
    sender_name.short_description = "Göndərən"
    
    def sender_email(self, obj):
        return obj.sender_email
    sender_email.short_description = "E-mail"


@admin.register(SocialMediaLink)
class SocialMediaLinkAdmin(admin.ModelAdmin):
    list_display = ['platform', 'url', 'is_active', 'is_hidden', 'order', 'created_at']
    list_filter = ['platform', 'is_active', 'is_hidden', 'created_at']
    list_editable = ['is_active', 'is_hidden', 'order']
    search_fields = ['platform', 'url']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Əsas məlumatlar', {
            'fields': ('platform', 'url', 'icon_class'),
            'description': 'Sosial media platforması və link məlumatları'
        }),
        ('Status', {
            'fields': ('is_active', 'is_hidden', 'order'),
            'description': 'Linkin aktiv olub-olmadığı və sırası'
        }),
        ('Tarix məlumatları', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
            'description': 'Linkin yaradılma və yenilənmə tarixləri'
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('order', 'platform')


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
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
            'fields': ('site_name', 'site_description', 'phone', 'email', 'address', 'is_active')
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
        return not SiteSettings.objects.exists()
    
    class Meta:
        verbose_name = "Logo"
        verbose_name_plural = "Logo"
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
