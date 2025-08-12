#!/usr/bin/env python3
"""
Logo məlumatlarını Logo modelindən SiteSettings modelinə köçürən script
"""

import os
import sys
import django

# Script-in yerləşdiyi qovluğu Python path-ə əlavə et
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Django environment-ini qur
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kitab_backend.settings')
django.setup()

from settings.models import SiteSettings, Logo

def migrate_logos():
    """Logo məlumatlarını Logo modelindən SiteSettings modelinə köçürür"""
    try:
        # Logo məlumatlarını al
        logo_settings = Logo.get_settings()
        print(f"Logo məlumatları tapıldı: {logo_settings.site_name}")
        
        # SiteSettings məlumatlarını al
        site_settings = SiteSettings.get_settings()
        print(f"SiteSettings məlumatları tapıldı: {site_settings.site_name}")
        
        # Logo məlumatlarını SiteSettings-ə köçür
        site_settings.navbar_logo = logo_settings.navbar_logo
        site_settings.navbar_logo_imagekit_url = logo_settings.navbar_logo_imagekit_url
        site_settings.footer_logo = logo_settings.footer_logo
        site_settings.footer_logo_imagekit_url = logo_settings.footer_logo_imagekit_url
        
        # Saxla
        site_settings.save()
        
        print("Logo məlumatları uğurla köçürüldü!")
        print(f"Navbar logo: {site_settings.navbar_logo}")
        print(f"Navbar logo ImageKit: {site_settings.navbar_logo_imagekit_url}")
        print(f"Footer logo: {site_settings.footer_logo}")
        print(f"Footer logo ImageKit: {site_settings.footer_logo_imagekit_url}")
        
    except Exception as e:
        print(f"Xəta baş verdi: {e}")

if __name__ == "__main__":
    migrate_logos() 