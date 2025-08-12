#!/usr/bin/env python
import os
import sys
import django

# Django settings-i yüklə
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kitab_backend.settings')
django.setup()

from settings.models import SiteSettings

def create_site_settings():
    """SiteSettings instance yaradır (statik məlumat olmadan)"""
    try:
        # Mövcud settings-ləri sil
        SiteSettings.objects.all().delete()
        
        # Yeni settings yaradır (sadece default dəyərlərlə)
        settings = SiteSettings.objects.create()
        
        print(f"✅ SiteSettings instance yaradıldı")
        print(f"ID: {settings.id}")
        print(f"Site Name: {settings.site_name}")
        print(f"Phone: {settings.phone}")
        print(f"Email: {settings.email}")
        print(f"Address: {settings.address}")
        print(f"Working Hours: {settings.working_hours}")
        print(f"Copyright Year: {settings.copyright_year}")
        print(f"Facebook: {settings.facebook}")
        print(f"Instagram: {settings.instagram}")
        print(f"Twitter: {settings.twitter}")
        print(f"YouTube: {settings.youtube}")
        print(f"WhatsApp: {settings.whatsapp_number}")
        print("\n💡 İndi Django admin'də bu məlumatları dəyişə bilərsiniz!")
        
    except Exception as e:
        print(f"❌ Xəta: {e}")

if __name__ == "__main__":
    create_site_settings() 