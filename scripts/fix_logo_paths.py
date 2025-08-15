#!/usr/bin/env python
"""
Logo fayl yollarını təmizləmək üçün script
Təkrarlanan qovluqlardakı faylları silir və düzgün yerlərə köçürür
"""

import os
import sys
import django
import shutil
from pathlib import Path

# Django settings-i yüklə
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kitab_backend.settings')
django.setup()

from django.conf import settings

def fix_logo_paths():
    """Təkrarlanan qovluqlardakı logo fayllarını təmizləyir"""
    
    media_root = Path(settings.MEDIA_ROOT)
    
    # Problemli qovluqlar
    problematic_paths = [
        'site/navbar/site/navbar_site/navbar',
        'site/footer/site/footer_site/footer',
        'site/navbar/site/navbar',
        'site/footer/site/footer',
    ]
    
    # Düzgün qovluqlar
    correct_paths = {
        'navbar': 'site/navbar',
        'footer': 'site/footer'
    }
    
    print("=== Logo fayl yollarını təmizləyirəm ===")
    
    for problematic_path in problematic_paths:
        full_path = media_root / problematic_path
        if full_path.exists():
            print(f"Problemli qovluq tapıldı: {problematic_path}")
            
            # Bu qovluqdakı faylları tap
            for file_path in full_path.rglob('*'):
                if file_path.is_file():
                    print(f"  Fayl tapıldı: {file_path.name}")
                    
                    # Faylın tipini müəyyən et
                    if 'navbar' in problematic_path:
                        target_folder = 'navbar'
                    elif 'footer' in problematic_path:
                        target_folder = 'footer'
                    else:
                        continue
                    
                    # Düzgün hədəf qovluğu yarat
                    target_path = media_root / correct_paths[target_folder]
                    target_path.mkdir(parents=True, exist_ok=True)
                    
                    # Faylı köçür
                    target_file = target_path / file_path.name
                    try:
                        shutil.copy2(file_path, target_file)
                        print(f"    ✅ Fayl köçürüldü: {target_file}")
                    except Exception as e:
                        print(f"    ❌ Fayl köçürülmədi: {e}")
            
            # Problemli qovluğu sil
            try:
                shutil.rmtree(full_path)
                print(f"  ✅ Problemli qovluq silindi: {problematic_path}")
            except Exception as e:
                print(f"  ❌ Qovluq silinmədi: {e}")
    
    print("=== Təmizləmə tamamlandı ===")

def check_media_structure():
    """Media qovluğunun strukturunu yoxlayır"""
    
    media_root = Path(settings.MEDIA_ROOT)
    
    print("\n=== Media qovluğunun cari strukturu ===")
    
    if media_root.exists():
        for item in sorted(media_root.rglob('*')):
            if item.is_dir():
                print(f"📁 {item.relative_to(media_root)}/")
            else:
                print(f"📄 {item.relative_to(media_root)}")
    else:
        print("Media qovluğu tapılmadı")

if __name__ == "__main__":
    print("Logo fayl yollarını təmizləyirəm...")
    
    # Əvvəlcə cari strukturu yoxla
    check_media_structure()
    
    # Problemi həll et
    fix_logo_paths()
    
    # Yenidən yoxla
    check_media_structure()
    
    print("\n✅ Script tamamlandı!") 