from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Author, Publisher, Book, BookReview
from .models import Banner

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'nationality', 'birth_date', 'death_date']
    list_filter = ['nationality', 'birth_date']
    search_fields = ['name', 'biography']
    date_hierarchy = 'birth_date'

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
        'is_active', 'is_featured', 'is_bestseller', 'sales_count'
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
            'fields': ('cover_image', 'back_image')
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

@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'rating', 'is_approved', 'created_at']
    list_filter = ['rating', 'is_approved', 'created_at']
    search_fields = ['book__title', 'user__username', 'comment']
    list_editable = ['is_approved']
    readonly_fields = ['created_at']

from .models import Banner

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "created_at")
    list_filter = ("is_active",)