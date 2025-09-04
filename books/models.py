from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    """Kitab kateqoriyaları"""
    name = models.CharField(max_length=100, verbose_name="Kateqoriya Adı")
    slug = models.SlugField(unique=True, verbose_name="URL Slug")
    description = models.TextField(blank=True, verbose_name="Təsvir")
    image = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name="Şəkil")
    imagekit_url = models.URLField(blank=True, null=True, verbose_name="ImageKit URL")
    imagekit_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="ImageKit ID")
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
    photo_imagekit_url = models.URLField(blank=True, null=True, verbose_name="Foto ImageKit URL")
    photo_imagekit_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="Foto ImageKit ID")
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
    
    # ImageKit URL-ləri
    cover_imagekit_url = models.URLField(blank=True, null=True, verbose_name="Üz qabığı ImageKit URL")
    back_imagekit_url = models.URLField(blank=True, null=True, verbose_name="Arxa qabıq ImageKit URL")
    cover_imagekit_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="Üz qabığı ImageKit ID")
    back_imagekit_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="Arxa qabıq ImageKit ID")
    
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
    
    def get_cover_image_url(self):
        """Üz qabığı şəklinin URL-ni qaytarır"""
        if self.cover_imagekit_url:
            return self.cover_imagekit_url
        elif self.cover_image:
            return self.cover_image.url
        return None
    
    def get_back_image_url(self):
        """Arxa qabıq şəklinin URL-ni qaytarır"""
        if self.back_imagekit_url:
            return self.back_imagekit_url
        elif self.back_image:
            return self.back_image.url
        return None
    
    def get_optimized_cover_url(self, width=None, height=None, quality=80):
        """Optimizasiya edilmiş üz qabığı URL-ni qaytarır"""
        if self.cover_imagekit_url:
            try:
                from lib.imagekit_utils import imagekit_manager
                filename = self.cover_imagekit_url.split('/')[-1]
                return imagekit_manager.optimize_image_url(filename, width, height, quality)
            except ImportError:
                print("Warning: lib.imagekit_utils not available, returning original URL")
                return self.get_cover_image_url()
        return self.get_cover_image_url()
    
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
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='book_reviews')
    anonymous_user = models.ForeignKey('users.AnonymousUser', on_delete=models.CASCADE, null=True, blank=True, related_name='book_reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Kitab Rəyi"
        verbose_name_plural = "Kitab Rəyləri"
    
    def __str__(self):
        user_name = self.user.get_full_name() if self.user else self.anonymous_user.display_name if self.anonymous_user else "Anonim"
        return f"{user_name} - {self.book.title} - {self.rating}/5"
    
    @property
    def user_name(self):
        """İstifadəçi adını qaytarır"""
        if self.user:
            return self.user.get_full_name() or self.user.username
        elif self.anonymous_user:
            return self.anonymous_user.display_name
        return "Anonim İstifadəçi"

from django.db import models

class Banner(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name="Başlıq")
    subtitle = models.CharField(max_length=300, blank=True, null=True, verbose_name="Alt başlıq")
    image = models.ImageField(upload_to='banners/', blank=True, null=True, verbose_name="Şəkil")
    imagekit_url = models.URLField(blank=True, null=True, verbose_name="ImageKit URL")
    imagekit_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="ImageKit ID")
    link = models.URLField(blank=True, verbose_name="Link")
    is_active = models.BooleanField(default=True, verbose_name="Aktiv")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Reklam Panosu"
        verbose_name_plural = "Reklam Panoları"

    def __str__(self):
        return self.title or f"Banner {self.id}"


