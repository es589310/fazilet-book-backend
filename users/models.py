from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

class UserProfile(models.Model):
    """İstifadəçi profili"""
    GENDER_CHOICES = [
        ('M', 'Kişi'),
        ('F', 'Qadın'),
        ('O', 'Digər'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="İstifadəçi")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Doğum Tarixi")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, verbose_name="Cins")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Avatar")
    
    # Ünvan məlumatları
    address = models.TextField(blank=True, verbose_name="Ünvan")
    city = models.CharField(max_length=100, blank=True, verbose_name="Şəhər")
    postal_code = models.CharField(max_length=10, blank=True, verbose_name="Poçt Kodu")
    
    # Preferences
    newsletter_subscription = models.BooleanField(default=True, verbose_name="Xəbər Bülleteni")
    sms_notifications = models.BooleanField(default=True, verbose_name="SMS Bildirişləri")
    email_notifications = models.BooleanField(default=True, verbose_name="E-mail Bildirişləri")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaradılma Tarixi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yenilənmə Tarixi")
    
    class Meta:
        verbose_name = "İstifadəçi Profili"
        verbose_name_plural = "İstifadəçi Profilləri"
    
    def __str__(self):
        return f"{self.user.username} - Profil"
    
    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """İstifadəçi yaradıldıqda avtomatik profil yarat"""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """İstifadəçi yenilənəndə profili də yenilə"""
    if hasattr(instance, 'profile'):
        instance.profile.save()

class Address(models.Model):
    """İstifadəçi ünvanları"""
    ADDRESS_TYPES = [
        ('home', 'Ev'),
        ('work', 'İş'),
        ('other', 'Digər'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name="İstifadəçi")
    title = models.CharField(max_length=100, verbose_name="Ünvan Başlığı")
    address_type = models.CharField(max_length=10, choices=ADDRESS_TYPES, default='home', verbose_name="Ünvan Növü")
    
    # Ünvan detalları
    full_address = models.TextField(verbose_name="Tam Ünvan")
    city = models.CharField(max_length=100, verbose_name="Şəhər")
    district = models.CharField(max_length=100, blank=True, verbose_name="Rayon")
    postal_code = models.CharField(max_length=10, blank=True, verbose_name="Poçt Kodu")
    
    # Contact
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    
    # Status
    is_default = models.BooleanField(default=False, verbose_name="Əsas Ünvan")
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaradılma Tarixi")
    
    class Meta:
        verbose_name = "Ünvan"
        verbose_name_plural = "Ünvanlar"
        ordering = ['-is_default', '-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    def save(self, *args, **kwargs):
        # Əgər bu ünvan əsas olaraq təyin edilirsə, digərlərini əsas olmaqdan çıxar
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)

# users/models.py
class AnonymousUser(models.Model):
    device_id = models.CharField(max_length=255, unique=True, verbose_name="Cihaz ID")
    display_name = models.CharField(max_length=100, default="", verbose_name="Görünən Ad")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaradılma Tarixi")
    last_activity = models.DateTimeField(auto_now=True, verbose_name="Son Aktivlik")
    
    class Meta:
        verbose_name = "Anonim İstifadəçi"
        verbose_name_plural = "Anonim İstifadəçilər"
    
    def __str__(self):
        return f"Anonim: {self.display_name or 'Bilinməyən'}"
    
    @classmethod
    def get_or_create_anonymous(cls, device_id):
        anonymous_user, created = cls.objects.get_or_create(
            device_id=device_id,
            defaults={
                'display_name': f"İstifadəçi {uuid.uuid4().hex[:8].upper()}"
            }
        )
        return anonymous_user