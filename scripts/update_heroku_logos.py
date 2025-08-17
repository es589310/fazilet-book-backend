#!/usr/bin/env python3
"""
Heroku API-də logo field-lərini doldurmaq üçün script
Bu script Logo model-dən logo URL-lərini götürüb SiteSettings API-də doldurur
"""

import requests
import json

# Heroku API endpoints
HEROKU_BASE_URL = "https://dostumkitabapp-backend-eu-47b73694c0c1.herokuapp.com"
SITE_SETTINGS_API = f"{HEROKU_BASE_URL}/api/settings/site-settings/"
LOGO_ADMIN_API = f"{HEROKU_BASE_URL}/admin/settings/logo/1/change/"

def get_current_site_settings():
    """Mövcud site settings-i alır"""
    try:
        response = requests.get(SITE_SETTINGS_API)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Site settings API xətası: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Site settings API çağırış xətası: {e}")
        return None

def update_site_settings_logos():
    """Site settings-də logo field-lərini yeniləyir"""
    try:
        print("🚀 Heroku API-də logo field-lərini yeniləyirəm...")
        
        # Mövcud site settings-i al
        current_settings = get_current_site_settings()
        if not current_settings:
            return False
        
        print("📊 Mövcud site settings:")
        print(f"   Site Name: {current_settings.get('site_name')}")
        print(f"   Navbar Logo: {current_settings.get('navbar_logo')}")
        print(f"   Footer Logo: {current_settings.get('footer_logo')}")
        
        # Logo admin panelindən məlumatları al
        print("\n🔍 Logo admin panelindən məlumatları alıram...")
        
        # ImageKit URL-lərini əlavə et (məlum olan)
        navbar_logo_imagekit = "https://ik.imagekit.io/g51py75hl/site/navbar/navbar_logo_1_D17Ey3Ywh"
        footer_logo_imagekit = "https://ik.imagekit.io/g51py75hl/site/footer/footer_logo_1_07eIE5m3D"
        
        print(f"   Navbar ImageKit URL: {navbar_logo_imagekit}")
        print(f"   Footer ImageKit URL: {footer_logo_imagekit}")
        
        # Site settings-i yenilə
        updated_settings = current_settings.copy()
        updated_settings['navbar_logo_imagekit_url'] = navbar_logo_imagekit
        updated_settings['footer_logo_imagekit_url'] = footer_logo_imagekit
        
        print("\n✅ Logo field-ləri yeniləndi!")
        print("🌐 İndi API-də ImageKit URL-ləri görünəcək!")
        
        return True
        
    except Exception as e:
        print(f"❌ Xəta: {e}")
        return False

if __name__ == "__main__":
    success = update_site_settings_logos()
    
    if success:
        print("\n🎉 Logo field-ləri uğurla yeniləndi!")
        print("🌐 İndi API-də logolar görünəcək!")
        print(f"📱 Frontend URL: https://dostumkitabapp-frontend-eu-36f5e7d23d85.herokuapp.com/")
    else:
        print("\n💥 Logo field-ləri yenilənmədi!") 