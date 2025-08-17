#!/usr/bin/env python3
"""
SiteSettings model-də logo field-lərini doldurmaq üçün script
Bu script Logo model-dən logo URL-lərini götürüb SiteSettings model-də doldurur
"""

import os
import sys
import django

# Django settings-i yüklə
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kitab_backend.settings')
django.setup()

from settings.models import SiteSettings, Logo

def update_site_settings_logos():
    """SiteSettings model-də logo field-lərini doldurur"""
    try:
        # Logo model-dən logo məlumatlarını al
        logo_settings = Logo.objects.first()
        if not logo_settings:
            print("❌ Logo model-də məlumat yoxdur!")
            return False
        
        # SiteSettings model-dən məlumatları al
        site_settings = SiteSettings.objects.get(id=1)
        
        print("📊 Mövcud məlumatlar:")
        print(f"   Logo Model - Navbar Logo: {logo_settings.navbar_logo}")
        print(f"   Logo Model - Footer Logo: {logo_settings.footer_logo}")
        print(f"   SiteSettings - Navbar Logo: {site_settings.navbar_logo}")
        print(f"   SiteSettings - Footer Logo: {site_settings.footer_logo}")
        
        # Logo field-lərini kopyala
        if logo_settings.navbar_logo:
            site_settings.navbar_logo = logo_settings.navbar_logo
            print(f"✅ Navbar logo kopyalandı: {logo_settings.navbar_logo}")
        
        if logo_settings.footer_logo:
            site_settings.footer_logo = logo_settings.footer_logo
            print(f"✅ Footer logo kopyalandı: {logo_settings.footer_logo}")
        
        # ImageKit URL-lərini də kopyala
        if logo_settings.navbar_logo_imagekit_url:
            site_settings.navbar_logo_imagekit_url = logo_settings.navbar_logo_imagekit_url
            print(f"✅ Navbar ImageKit URL kopyalandı: {logo_settings.navbar_logo_imagekit_url}")
        
        if logo_settings.footer_logo_imagekit_url:
            site_settings.footer_logo_imagekit_url = logo_settings.footer_logo_imagekit_url
            print(f"✅ Footer ImageKit URL kopyalandı: {logo_settings.footer_logo_imagekit_url}")
        
        # Save et
        site_settings.save()
        print("✅ SiteSettings model-i yeniləndi!")
        
        # Yoxla
        print("\n📊 Yenilənmiş məlumatlar:")
        print(f"   SiteSettings - Navbar Logo: {site_settings.navbar_logo}")
        print(f"   SiteSettings - Footer Logo: {site_settings.footer_logo}")
        print(f"   SiteSettings - Navbar ImageKit URL: {site_settings.navbar_logo_imagekit_url}")
        print(f"   SiteSettings - Footer ImageKit URL: {site_settings.footer_logo_imagekit_url}")
        
        return True
        
    except Exception as e:
        print(f"❌ Xəta: {e}")
        return False

if __name__ == "__main__":
    print("🚀 SiteSettings logo field-lərini yeniləyirəm...")
    success = update_site_settings_logos()
    
    if success:
        print("\n🎉 Logo field-ləri uğurla yeniləndi!")
        print("🌐 İndi API-də logolar görünəcək!")
    else:
        print("\n💥 Logo field-ləri yenilənmədi!") 