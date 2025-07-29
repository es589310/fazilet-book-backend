from django.db import models
from django.contrib.auth.models import User
from books.models import Book
from users.models import Address
from decimal import Decimal

class Cart(models.Model):
    """Alış-veriş səbəti"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart', verbose_name="İstifadəçi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaradılma Tarixi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yenilənmə Tarixi")
    
    class Meta:
        verbose_name = "Səbət"
        verbose_name_plural = "Səbətlər"
    
    def __str__(self):
        return f"{self.user.username} - Səbət"
    
    @property
    def total_price(self):
        """Səbətin ümumi qiyməti"""
        return sum(item.total_price for item in self.items.all())
    
    @property
    def total_items(self):
        """Səbətdəki ümumi məhsul sayı"""
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    """Səbət elementləri"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name="Səbət")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Kitab")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Miqdar")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Əlavə Edilmə Tarixi")
    
    class Meta:
        verbose_name = "Səbət Elementi"
        verbose_name_plural = "Səbət Elementləri"
        unique_together = ['cart', 'book']
    
    def __str__(self):
        return f"{self.cart.user.username} - {self.book.title} ({self.quantity})"
    
    @property
    def total_price(self):
        """Bu elementin ümumi qiyməti"""
        return self.book.price * self.quantity

class Order(models.Model):
    """Sifarişlər"""
    STATUS_CHOICES = [
        ('pending', 'Gözləyir'),
        ('confirmed', 'Təsdiqləndi'),
        ('processing', 'Hazırlanır'),
        ('shipped', 'Göndərildi'),
        ('delivered', 'Çatdırıldı'),
        ('cancelled', 'Ləğv Edildi'),
        ('returned', 'Qaytarıldı'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Gözləyir'),
        ('paid', 'Ödənildi'),
        ('failed', 'Uğursuz'),
        ('refunded', 'Geri Qaytarıldı'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Nağd'),
        ('card', 'Kart'),
        ('bank_transfer', 'Bank Köçürməsi'),
        ('online', 'Onlayn Ödəniş'),
    ]
    
    # Sifariş məlumatları
    order_number = models.CharField(max_length=20, unique=True, verbose_name="Sifariş Nömrəsi")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name="İstifadəçi")
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Status")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending', verbose_name="Ödəniş Statusu")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash', verbose_name="Ödəniş Üsulu")
    
    # Qiymət məlumatları
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ara Cəm")
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Çatdırılma Qiyməti")
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Endirim Məbləği")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ümumi Məbləğ")
    
    # Çatdırılma məlumatları
    delivery_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, verbose_name="Çatdırılma Ünvanı")
    delivery_name = models.CharField(max_length=200, verbose_name="Alıcı Adı")
    delivery_phone = models.CharField(max_length=20, verbose_name="Alıcı Telefonu")
    delivery_address_text = models.TextField(verbose_name="Çatdırılma Ünvanı (Mətn)")
    
    # Qeydlər
    notes = models.TextField(blank=True, verbose_name="Qeydlər")
    admin_notes = models.TextField(blank=True, verbose_name="Admin Qeydləri")
    
    # Tarixlər
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Sifariş Tarixi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yenilənmə Tarixi")
    shipped_at = models.DateTimeField(null=True, blank=True, verbose_name="Göndərilmə Tarixi")
    delivered_at = models.DateTimeField(null=True, blank=True, verbose_name="Çatdırılma Tarixi")
    
    class Meta:
        verbose_name = "Sifariş"
        verbose_name_plural = "Sifarişlər"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Sifariş #{self.order_number} - {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            # Sifariş nömrəsi yaradırıq
            import uuid
            self.order_number = f"KS{str(uuid.uuid4())[:8].upper()}"
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    """Sifariş elementləri"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Sifariş")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Kitab")
    quantity = models.PositiveIntegerField(verbose_name="Miqdar")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Qiymət")
    
    class Meta:
        verbose_name = "Sifariş Elementi"
        verbose_name_plural = "Sifariş Elementləri"
    
    def __str__(self):
        return f"{self.order.order_number} - {self.book.title}"
    
    @property
    def total_price(self):
        """Bu elementin ümumi qiyməti"""
        return self.price * self.quantity

class OrderStatusHistory(models.Model):
    """Sifariş status tarixçəsi"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history', verbose_name="Sifariş")
    status = models.CharField(max_length=20, choices=Order.STATUS_CHOICES, verbose_name="Status")
    notes = models.TextField(blank=True, verbose_name="Qeydlər")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dəyişiklik Tarixi")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Dəyişdirən")
    
    class Meta:
        verbose_name = "Status Tarixçəsi"
        verbose_name_plural = "Status Tarixçələri"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.order.order_number} - {self.get_status_display()}"
