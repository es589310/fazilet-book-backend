from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
from .models import SiteSettings
from lib.imagekit_utils import upload_logo_to_imagekit, delete_logo_from_imagekit
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=SiteSettings)
def handle_logo_upload(sender, instance, created, **kwargs):
    """
    Logo-lar yükləndikdə avtomatik ImageKit-ə yükləyir
    """
    print(f"Logo upload signal triggered for {instance.site_name}")
    
    # Navbar logo yüklə
    if instance.navbar_logo and hasattr(instance.navbar_logo, 'path'):
        print(f"Processing navbar logo: {instance.navbar_logo.path}")
        if created or instance.navbar_logo_imagekit_url != instance.navbar_logo.url:
            result = upload_logo_to_imagekit(instance.navbar_logo, 'site/navbar')
            print(f"Navbar logo upload result: {result}")
            
            if result['success']:
                SiteSettings.objects.filter(pk=instance.pk).update(
                    navbar_logo_imagekit_url=result['url']
                )
                print(f"Updated navbar logo URL: {result['url']}")
            else:
                print(f"Navbar logo upload failed: {result.get('error')}")
    
    # Footer logo yüklə
    if instance.footer_logo and hasattr(instance.footer_logo, 'path'):
        print(f"Processing footer logo: {instance.footer_logo.path}")
        if created or instance.footer_logo_imagekit_url != instance.footer_logo.url:
            result = upload_logo_to_imagekit(instance.footer_logo, 'site/footer')
            print(f"Footer logo upload result: {result}")
            
            if result['success']:
                SiteSettings.objects.filter(pk=instance.pk).update(
                    footer_logo_imagekit_url=result['url']
                )
                print(f"Updated footer logo URL: {result['url']}")
            else:
                print(f"Footer logo upload failed: {result.get('error')}")

@receiver(pre_delete, sender=SiteSettings)
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