from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class SiteSettings(models.Model):
    """Sayt üçün əsas tənzimləmələr"""
    site_name = models.CharField(max_length=100, default="Fəzilət Kitab", verbose_name="Sayt adı")
    site_description = models.TextField(blank=True, verbose_name="Sayt təsviri")
    
    # Navbar logo
    navbar_logo = models.ImageField(upload_to='site/navbar/', blank=True, null=True, verbose_name="Navbar Logo")
    navbar_logo_imagekit_url = models.URLField(blank=True, null=True, verbose_name="Navbar Logo ImageKit URL")
    
    # Footer logo
    footer_logo = models.ImageField(upload_to='site/footer/', blank=True, null=True, verbose_name="Footer Logo")
    footer_logo_imagekit_url = models.URLField(blank=True, null=True, verbose_name="Footer Logo ImageKit URL")
    
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    email = models.EmailField(blank=True, verbose_name="E-mail")
    address = models.TextField(blank=True, verbose_name="Ünvan")
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
        if not self.pk and SiteSettings.objects.exists():
            return
        
        # Media URL-lərini avtomatik doldur
        if self.navbar_logo and not self.navbar_logo_imagekit_url:
            try:
                # Media URL-ni istifadə et
                self.navbar_logo_imagekit_url = self.navbar_logo.url
            except Exception:
                self.navbar_logo_imagekit_url = None
        
        if self.footer_logo and not self.footer_logo_imagekit_url:
            try:
                # Media URL-ni istifadə et
                self.footer_logo_imagekit_url = self.footer_logo.url
            except Exception:
                self.footer_logo_imagekit_url = None
        
        super().save(*args, **kwargs)


class ContactMessage(models.Model):
    MESSAGE_STATUS = (
        ('pending', 'Gözləyir'),
        ('sent', 'Göndərildi'),
        ('replied', 'Cavablandırıldı'),
        ('failed', 'Xəta'),
    )
    
    # İstifadəçi girişi olmayanlar üçün
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ad Soyad")
    email = models.EmailField(blank=True, null=True, verbose_name="E-mail")
    
    # Giriş etmiş istifadəçilər üçün
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="İstifadəçi")
    
    # Ümumi sahələr
    subject = models.CharField(max_length=200, verbose_name="Mövzu")
    message = models.TextField(verbose_name="Mesaj")
    status = models.CharField(max_length=20, choices=MESSAGE_STATUS, default='pending', verbose_name="Status")
    
    # Avtomatik cavab
    auto_reply_sent = models.BooleanField(default=False, verbose_name="Avtomatik cavab göndərildi")
    auto_reply_date = models.DateTimeField(blank=True, null=True, verbose_name="Avtomatik cavab tarixi")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaradılma tarixi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yenilənmə tarixi")
    
    class Meta:
        verbose_name = "Əlaqə mesajı"
        verbose_name_plural = "Əlaqə mesajları"
        ordering = ['-created_at']
    
    def __str__(self):
        if self.user:
            return f"{self.user.get_full_name()} - {self.subject}"
        else:
            return f"{self.name} - {self.subject}"
    
    @property
    def sender_name(self):
        """Göndərənin adını qaytarır"""
        if self.user:
            return self.user.get_full_name() or self.user.username
        return self.name
    
    @property
    def sender_email(self):
        """Göndərənin email-ini qaytarır"""
        if self.user:
            return self.user.email
        return self.email


class SocialMediaLink(models.Model):
    """Sosial media linkləri üçün model"""
    PLATFORM_CHOICES = (
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter'),
        ('youtube', 'YouTube'),
        ('linkedin', 'LinkedIn'),
        ('telegram', 'Telegram'),
    )
    
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, verbose_name="Platforma")
    url = models.URLField(verbose_name="Link")
    icon_class = models.CharField(max_length=100, blank=True, verbose_name="İkon CSS sinifi")
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    is_hidden = models.BooleanField(default=False, verbose_name="Gizlət")
    order = models.PositiveIntegerField(default=0, verbose_name="Sıra")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaradılma tarixi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yenilənmə tarixi")
    
    class Meta:
        verbose_name = "Sosial media linki"
        verbose_name_plural = "Sosial media linkləri"
        ordering = ['order', 'platform']
        unique_together = ['platform']
    
    def __str__(self):
        return f"{self.get_platform_display()} - {self.url}"
    
    def get_icon_class(self):
        """Platforma üçün default ikon sinifini qaytarır"""
        if self.icon_class:
            return self.icon_class
        
        icon_map = {
            'facebook': 'fab fa-facebook-f',
            'instagram': 'fab fa-instagram',
            'twitter': 'fab fa-twitter',
            'youtube': 'fab fa-youtube',
            'linkedin': 'fab fa-linkedin-in',
            'telegram': 'fab fa-telegram-plane',
        }
        return icon_map.get(self.platform, 'fas fa-link')
