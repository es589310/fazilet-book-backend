#!/usr/bin/env python
import os
import sys
import django

# Django settings-i yüklə
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kitab_backend.settings')
django.setup()

from books.models import Banner

def create_sample_banner():
    """Nümunə banner yaradır"""
    try:
        # Mövcud bannerləri sil
        Banner.objects.all().delete()
        
        # Yeni banner yaradır
        banner = Banner.objects.create(
            title="Yeni Kitablar",
            subtitle="Ən yaxşı kitablar sizin üçün",
            image="banners/sample-banner.jpg",  # Bu şəkil media/banners/ qovluğunda olmalıdır
            link="https://example.com",
            is_active=True
        )
        
        print(f"Banner yaradıldı: {banner.title}")
        print(f"ID: {banner.id}")
        print(f"Aktiv: {banner.is_active}")
        
    except Exception as e:
        print(f"Xəta: {e}")

if __name__ == "__main__":
    create_sample_banner() 