from django.db import models

# Create your models here.

class SiteSettings(models.Model):
    """Sayt tənzimləmələri"""
    site_name = models.CharField(max_length=200, default="Fəzilət Kitab", verbose_name="Sayt Adı")
    site_description = models.TextField(default="Azərbaycanda ən böyük onlayn kitab mağazası. Minlərlə kitab, ən yaxşı qiymətlər və sürətli çatdırılma xidməti.", verbose_name="Sayt Təsviri")
    
    phone = models.CharField(max_length=20, default="+994 12 345 67 89", verbose_name="Telefon")
    email = models.EmailField(default="info@faziletkitab.az", verbose_name="E-mail")
    address = models.TextField(blank=True, verbose_name="Ünvan")
    working_hours = models.CharField(max_length=100, default="Bazar ertəsi - Cümə: 09:00-18:00", verbose_name="İş Saatları")
    copyright_year = models.IntegerField(default=2024, verbose_name="Copyright İli")
    facebook = models.URLField(blank=True, verbose_name="Facebook")
    instagram = models.URLField(blank=True, verbose_name="Instagram")
    twitter = models.URLField(blank=True, verbose_name="Twitter")
    youtube = models.URLField(blank=True, verbose_name="YouTube")
    whatsapp_number = models.CharField(max_length=20, default="+994501234567", verbose_name="WhatsApp Nömrəsi")
    
    # Logo sahələri
    navbar_logo = models.ImageField(upload_to='site/navbar/', blank=True, null=True, verbose_name="Navbar Logo")
    navbar_logo_imagekit_url = models.URLField(blank=True, null=True, verbose_name="Navbar Logo ImageKit URL")
    footer_logo = models.ImageField(upload_to='site/footer/', blank=True, null=True, verbose_name="Footer Logo")
    footer_logo_imagekit_url = models.URLField(blank=True, null=True, verbose_name="Footer Logo ImageKit URL")
    
    class Meta:
        verbose_name = "Tənzimləmə"
        verbose_name_plural = "Tənzimləmə"
    
    def __str__(self):
        return f"{self.site_name} - Tənzimləmə"
    
    @classmethod
    def get_settings(cls):
        """Tək instance qaytarır"""
        settings, created = cls.objects.get_or_create(id=1)
        return settings


class Logo(models.Model):
    """Sayt üçün logo tənzimləmələri"""
    site_name = models.CharField(max_length=100, default="Fəzilət Kitab", verbose_name="Sayt adı")
    
    # Navbar logo
    navbar_logo = models.ImageField(upload_to='site/navbar/', blank=True, null=True, verbose_name="Navbar Logo")
    navbar_logo_imagekit_url = models.URLField(blank=True, null=True, verbose_name="Navbar Logo ImageKit URL")
    
    # Footer logo
    footer_logo = models.ImageField(upload_to='site/footer/', blank=True, null=True, verbose_name="Footer Logo")
    footer_logo_imagekit_url = models.URLField(blank=True, null=True, verbose_name="Footer Logo ImageKit URL")
    
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaradılma tarixi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yenilənmə tarixi")
    
    class Meta:
        verbose_name = "Logo"
        verbose_name_plural = "Logo"
    
    def __str__(self):
        return f"{self.site_name} - Logo"
    
    def save(self, *args, **kwargs):
        # Əgər yalnız bir tənzimləmə olsun
        if not self.pk and Logo.objects.exists():
            return
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """Tək instance qaytarır"""
        settings, created = cls.objects.get_or_create(id=1)
        return settings
