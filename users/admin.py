from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Address

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profil'

class AddressInline(admin.TabularInline):
    model = Address
    extra = 0

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, AddressInline)
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']
    list_per_page = 25
    ordering = ['-date_joined']
    date_hierarchy = 'date_joined'
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

# Django-nun əsas User modelini yenidən qeydiyyatdan keçiririk
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'address_type', 'city', 'is_default', 'is_active']
    list_filter = ['address_type', 'city', 'is_default', 'is_active']
    search_fields = ['user__username', 'title', 'full_address', 'city']
    list_editable = ['is_default', 'is_active']
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
