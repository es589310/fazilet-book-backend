from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
