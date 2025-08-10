from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Author, Publisher, Book, BookReview, Banner, SiteSettings

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'image_display', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']
    
    fieldsets = (
        ('Əsas Məlumatlar', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Şəkil', {
            'fields': ('image', 'imagekit_url')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def image_display(self, obj):
        """Kateqoriya şəklinin admin panelində göstərilməsi"""
        if obj.imagekit_url:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.imagekit_url)
        elif obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "Şəkil yoxdur"
    image_display.short_description = "Şəkil"
    
    def save_model(self, request, obj, form, change):
        """Şəkli ImageKit-ə yükləyir"""
        super().save_model(request, obj, form, change)
        
        if 'image' in form.changed_data and obj.image:
            from lib.imagekit_utils import imagekit_manager
            result = imagekit_manager.upload_image(
                obj.image, 
                folder_path='categories',
                filename=f"category_{obj.slug}_{obj.id}"
            )
            if result['success']:
                obj.imagekit_url = result['url']
                obj.imagekit_id = result['file_id']
                obj.save(update_fields=['imagekit_url', 'imagekit_id'])

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'photo_display', 'nationality', 'birth_date', 'death_date']
    list_filter = ['nationality', 'birth_date']
    search_fields = ['name', 'biography']
    date_hierarchy = 'birth_date'
    
    def photo_display(self, obj):
        """Müəllif şəklinin admin panelində göstərilməsi"""
        if obj.photo_imagekit_url:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.photo_imagekit_url)
        elif obj.photo:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.photo.url)
        return "Şəkil yoxdur"
    photo_display.short_description = "Foto"
    
    def save_model(self, request, obj, form, change):
        """Şəkli ImageKit-ə yükləyir"""
        super().save_model(request, obj, form, change)
        
        if 'photo' in form.changed_data and obj.photo:
            from lib.imagekit_utils import imagekit_manager
            result = imagekit_manager.upload_image(
                obj.photo, 
                folder_path='authors',
                filename=f"author_{obj.id}_{obj.name.replace(' ', '_')}"
            )
            if result['success']:
                obj.photo_imagekit_url = result['url']
                obj.photo_imagekit_id = result['file_id']
                obj.save(update_fields=['photo_imagekit_url', 'photo_imagekit_id'])

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'website']
    search_fields = ['name', 'address']

class BookReviewInline(admin.TabularInline):
    model = BookReview
    extra = 0
    readonly_fields = ['user', 'rating', 'comment', 'created_at']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'publisher', 'price', 'stock_quantity', 
        'is_active', 'is_featured', 'is_bestseller', 'sales_count', 'cover_image_display'
    ]
    list_filter = [
        'category', 'publisher', 'language', 'is_active', 
        'is_featured', 'is_bestseller', 'is_new', 'created_at'
    ]
    search_fields = ['title', 'isbn', 'description']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['price', 'stock_quantity', 'is_active', 'is_featured', 'is_bestseller']
    filter_horizontal = ['authors']
    inlines = [BookReviewInline]
    
    fieldsets = (
        ('Əsas Məlumatlar', {
            'fields': ('title', 'slug', 'authors', 'category', 'publisher')
        }),
        ('Kitab Detalları', {
            'fields': ('isbn', 'description', 'language', 'pages', 'publication_date')
        }),
        ('Qiymət və Stok', {
            'fields': ('price', 'original_price', 'stock_quantity')
        }),
        ('Şəkillər', {
            'fields': ('cover_image', 'back_image', 'cover_imagekit_url', 'back_imagekit_url')
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured', 'is_bestseller', 'is_new')
        }),
        ('Statistika', {
            'fields': ('views_count', 'sales_count'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['views_count', 'sales_count']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category', 'publisher')
    
    def cover_image_display(self, obj):
        """Üz qabığı şəklinin admin panelində göstərilməsi"""
        if obj.cover_imagekit_url:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.cover_imagekit_url)
        elif obj.cover_image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.cover_image.url)
        return "Şəkil yoxdur"
    cover_image_display.short_description = "Üz Qabığı"
    
    def save_model(self, request, obj, form, change):
        """Şəkilləri ImageKit-ə yükləyir"""
        super().save_model(request, obj, form, change)
        
        # Cover image yüklənməsi
        if 'cover_image' in form.changed_data and obj.cover_image:
            from lib.imagekit_utils import imagekit_manager
            result = imagekit_manager.upload_image(
                obj.cover_image, 
                folder_path='books/covers',
                filename=f"cover_{obj.slug}_{obj.id}"
            )
            if result['success']:
                obj.cover_imagekit_url = result['url']
                obj.cover_imagekit_id = result['file_id']
                obj.save(update_fields=['cover_imagekit_url', 'cover_imagekit_id'])
        
        # Back image yüklənməsi
        if 'back_image' in form.changed_data and obj.back_image:
            from lib.imagekit_utils import imagekit_manager
            result = imagekit_manager.upload_image(
                obj.back_image, 
                folder_path='books/backs',
                filename=f"back_{obj.slug}_{obj.id}"
            )
            if result['success']:
                obj.back_imagekit_url = result['url']
                obj.back_imagekit_id = result['file_id']
                obj.save(update_fields=['back_imagekit_url', 'back_imagekit_id'])

@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    list_display = ("book", "user_name", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("book__title", "comment")
    readonly_fields = ("created_at",)
    
    def user_name(self, obj):
        return obj.user_name
    user_name.short_description = "İstifadəçi"

from .models import Banner

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("title", "image_display", "is_active", "created_at")
    list_filter = ("is_active",)
    
    def image_display(self, obj):
        """Banner şəklinin admin panelində göstərilməsi"""
        if obj.imagekit_url:
            return format_html('<img src="{}" width="100" height="50" style="object-fit: cover;" />', obj.imagekit_url)
        elif obj.image:
            return format_html('<img src="{}" width="100" height="50" style="object-fit: cover;" />', obj.image.url)
        return "Şəkil yoxdur"
    image_display.short_description = "Şəkil"
    
    def save_model(self, request, obj, form, change):
        """Şəkli ImageKit-ə yükləyir"""
        super().save_model(request, obj, form, change)
        
        if 'image' in form.changed_data and obj.image:
            from lib.imagekit_utils import imagekit_manager
            result = imagekit_manager.upload_image(
                obj.image, 
                folder_path='banners',
                filename=f"banner_{obj.id}_{obj.title.replace(' ', '_')}"
            )
            if result['success']:
                obj.imagekit_url = result['url']
                obj.imagekit_id = result['file_id']
                obj.save(update_fields=['imagekit_url', 'imagekit_id'])

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'phone', 'email', 'whatsapp_number', 'copyright_year']
    fieldsets = (
        ('Əsas Məlumatlar', {
            'fields': ('site_name', 'site_description')
        }),
        ('Əlaqə Məlumatları', {
            'fields': ('phone', 'email', 'address', 'working_hours', 'whatsapp_number')
        }),
        ('Copyright', {
            'fields': ('copyright_year',)
        }),
        ('Sosial Media', {
            'fields': ('facebook', 'instagram', 'twitter', 'youtube'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Yalnız bir instance ola bilər
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Silməyə icazə vermə
        return False