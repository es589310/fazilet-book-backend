from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['sender_name', 'sender_email', 'subject', 'status', 'created_at', 'auto_reply_sent']
    list_filter = ['status', 'auto_reply_sent', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message', 'user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Göndərən məlumatları', {
            'fields': ('user', 'name', 'email')
        }),
        ('Mesaj məlumatları', {
            'fields': ('subject', 'message', 'status')
        }),
        ('Avtomatik cavab', {
            'fields': ('auto_reply_sent', 'auto_reply_date')
        }),
        ('Tarix məlumatları', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def sender_name(self, obj):
        return obj.sender_name
    sender_name.short_description = "Göndərən"
    
    def sender_email(self, obj):
        return obj.sender_email
    sender_email.short_description = "E-mail"
