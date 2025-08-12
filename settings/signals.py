from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
from .models import SiteSettings, Logo
from lib.imagekit_utils import upload_logo_to_imagekit, delete_logo_from_imagekit
import logging
import os

logger = logging.getLogger(__name__)

# SiteSettings üçün logo signal'ini sildim çünki SiteSettings modelində logo field'ları yox

@receiver(post_save, sender=Logo)
def handle_logo_upload(sender, instance, created, **kwargs):
    """
    Logo-lar yükləndikdə avtomatik ImageKit-ə yükləyir
    Bu signal admin-dəki save_model metodu ilə birlikdə işləyir
    """
    print(f"=== Logo upload signal triggered for {instance.site_name} ===")
    print(f"Instance ID: {instance.pk}")
    print(f"Created: {created}")
    
    # Navbar logo yüklə
    if instance.navbar_logo and hasattr(instance.navbar_logo, 'path'):
        print(f"=== Processing Navbar Logo ===")
        print(f"Navbar logo path: {instance.navbar_logo.path}")
        print(f"Navbar logo exists: {os.path.exists(instance.navbar_logo.path)}")
        
        # Əgər ImageKit URL-i yoxdursa və ya dəyişibsə yüklə
        if not instance.navbar_logo_imagekit_url or created:
            print("Uploading navbar logo to ImageKit via signal...")
            result = upload_logo_to_imagekit(instance.navbar_logo, 'site/navbar')
            print(f"Navbar logo upload result: {result}")
            
            if result['success']:
                Logo.objects.filter(pk=instance.pk).update(
                    navbar_logo_imagekit_url=result['url']
                )
                print(f"✅ Successfully updated navbar logo URL via signal: {result['url']}")
            else:
                print(f"❌ Navbar logo upload failed via signal: {result.get('error')}")
        else:
            print("Navbar logo already has ImageKit URL")
    
    # Footer logo yüklə
    if instance.footer_logo and hasattr(instance.footer_logo, 'path'):
        print(f"=== Processing Footer Logo ===")
        print(f"Footer logo path: {instance.footer_logo.path}")
        print(f"Footer logo exists: {os.path.exists(instance.footer_logo.path)}")
        
        # Əgər ImageKit URL-i yoxdursa və ya dəyişibsə yüklə
        if not instance.footer_logo_imagekit_url or created:
            print("Uploading footer logo to ImageKit via signal...")
            result = upload_logo_to_imagekit(instance.footer_logo, 'site/footer')
            print(f"Footer logo upload result: {result}")
            
            if result['success']:
                Logo.objects.filter(pk=instance.pk).update(
                    footer_logo_imagekit_url=result['url']
                )
                print(f"✅ Successfully updated footer logo URL via signal: {result['url']}")
            else:
                print(f"❌ Footer logo upload failed via signal: {result.get('error')}")
        else:
            print("Footer logo already has ImageKit URL")
    
    print(f"=== Logo signal processing completed ===")

@receiver(pre_delete, sender=Logo)
def handle_logo_deletion(sender, instance, **kwargs):
    """
    Logo-lar silindikdə ImageKit-dən də silir
    """
    # Navbar logo sil
    if instance.navbar_logo_imagekit_url:
        file_id = instance.navbar_logo_imagekit_url.split('/')[-1].split('?')[0]
        delete_logo_from_imagekit(file_id)
    
    # Footer logo sil
    if instance.footer_logo_imagekit_url:
        file_id = instance.footer_logo_imagekit_url.split('/')[-1].split('?')[0]
        delete_logo_from_imagekit(file_id) 