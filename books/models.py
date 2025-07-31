from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    """Kitab kateqoriyaları"""
    name = models.CharField(max_length=100, verbose_name="Kateqoriya Adı")
    slug = models.SlugField(unique=True, verbose_name="URL Slug")
    description = models.TextField(blank=True, verbose_name="Təsvir")
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="Şəkil")
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaradılma Tarixi")
    
    class Meta:
        verbose_name = "Kateqoriya"
        verbose_name_plural = "Kateqoriyalar"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Author(models.Model):
    """Müəlliflər"""
    name = models.CharField(max_length=200, verbose_name="Ad Soyad")
    biography = models.TextField(blank=True, verbose_name="Bioqrafiya")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Doğum Tarixi")
    death_date = models.DateField(blank=True, null=True, verbose_name="Vəfat Tarixi")
    photo = models.ImageField(upload_to='authors/', blank=True, null=True, verbose_name="Foto")
    nationality = models.CharField(max_length=100, blank=True, verbose_name="Milliyyət")
    
    class Meta:
        verbose_name = "Müəllif"
        verbose_name_plural = "Müəlliflər"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Publisher(models.Model):
    """Nəşriyyatlar"""
    name = models.CharField(max_length=200, verbose_name="Nəşriyyat Adı")
    address = models.TextField(blank=True, verbose_name="Ünvan")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefon")
    email = models.EmailField(blank=True, verbose_name="E-mail")
    website = models.URLField(blank=True, verbose_name="Veb sayt")
    
    class Meta:
        verbose_name = "Nəşriyyat"
        verbose_name_plural = "Nəşriyyatlar"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Book(models.Model):
    """Kitablar"""
    LANGUAGE_CHOICES = [
        ('az', 'Azərbaycan'),
        ('tr', 'Türk'),
        ('en', 'İngilis'),
        ('ru', 'Rus'),
        ('ar', 'Ərəb'),
        ('fa', 'Fars'),
        ('other', 'Digər'),
    ]
    
    title = models.CharField(max_length=300, verbose_name="Kitab Adı")
    slug = models.SlugField(unique=True, verbose_name="URL Slug")
    authors = models.ManyToManyField(Author, verbose_name="Müəlliflər")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Kateqoriya")
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, verbose_name="Nəşriyyat")
    
    # Kitab məlumatları
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True, verbose_name="ISBN")
    description = models.TextField(verbose_name="Təsvir")
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='az', verbose_name="Dil")
    pages = models.PositiveIntegerField(verbose_name="Səhifə Sayı")
    publication_date = models.DateField(verbose_name="Nəşr Tarixi")
    
    # Qiymət və stok
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Qiymət (₼)")
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Orijinal Qiymət (₼)")
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name="Stok Miqdarı")
    
    # Şəkillər
    cover_image = models.ImageField(upload_to='books/covers/', verbose_name="Üz qabığı")
    back_image = models.ImageField(upload_to='books/backs/', blank=True, null=True, verbose_name="Arxa qabıq")
    
    # Status və reytinq
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    is_featured = models.BooleanField(default=False, verbose_name="Seçilmiş")
    is_bestseller = models.BooleanField(default=False, verbose_name="Bestseller")
    is_new = models.BooleanField(default=False, verbose_name="Yeni")
    
    # Metadata
    views_count = models.PositiveIntegerField(default=0, verbose_name="Baxış Sayı")
    sales_count = models.PositiveIntegerField(default=0, verbose_name="Satış Sayı")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Əlavə Edilmə Tarixi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yenilənmə Tarixi")
    
    class Meta:
        verbose_name = "Kitab"
        verbose_name_plural = "Kitablar"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def discount_percentage(self):
        """Endirim faizini hesabla"""
        if self.original_price and self.original_price > self.price:
            return int(((self.original_price - self.price) / self.original_price) * 100)
        return 0
    
    @property
    def average_rating(self):
        """Orta reytinqi hesabla"""
        reviews = self.reviews.all()
        if reviews:
            return sum([review.rating for review in reviews]) / len(reviews)
        return 0
    
    @property
    def reviews_count(self):
        """Rəy sayını qaytarır"""
        return self.reviews.count()

class BookReview(models.Model):
    """Kitab rəyləri"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews', verbose_name="Kitab")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="İstifadəçi")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Reytinq"
    )
    comment = models.TextField(verbose_name="Rəy")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaradılma Tarixi")
    is_approved = models.BooleanField(default=True, verbose_name="Təsdiqlənmiş")
    
    class Meta:
        verbose_name = "Kitab Rəyi"
        verbose_name_plural = "Kitab Rəyləri"
        ordering = ['-created_at']
        # unique_together kaldırıldı - kullanıcılar birden fazla rəy yazabilir
    
    def __str__(self):
        return f"{self.book.title} - {self.user.username} ({self.rating}/5)"

from django.db import models

class Banner(models.Model):
    title = models.CharField(max_length=200, verbose_name="Başlıq")
    subtitle = models.CharField(max_length=300, blank=True, verbose_name="Alt başlıq")
    image = models.ImageField(upload_to='banners/', verbose_name="Şəkil")
    link = models.URLField(blank=True, verbose_name="Link")
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Reklam Panosu"
        verbose_name_plural = "Reklam Panoları"

    def __str__(self):
        return self.title
