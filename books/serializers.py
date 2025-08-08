from rest_framework import serializers
from .models import Category, Author, Publisher, Book, BookReview, Banner, SiteSettings

class CategorySerializer(serializers.ModelSerializer):
    books_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'is_active', 'books_count']
    
    def get_books_count(self, obj):
        return obj.book_set.count()

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'biography', 'birth_date', 'death_date', 'photo', 'nationality']

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'address', 'phone', 'email', 'website']

class BookReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = BookReview
        fields = ['id', 'rating', 'comment', 'created_at', 'user_name']
        read_only_fields = ['id', 'created_at', 'user_name']
    
    def get_user_name(self, obj):
        return obj.user_name
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            validated_data['user'] = request.user
        elif request and hasattr(request, 'anonymous_user'):
            validated_data['anonymous_user'] = request.anonymous_user
        return super().create(validated_data)

class BookListSerializer(serializers.ModelSerializer):
    """Kitab siyahısı üçün sadə serializer"""
    authors = AuthorSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    average_rating = serializers.ReadOnlyField()
    reviews_count = serializers.ReadOnlyField()
    discount_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'slug', 'authors', 'category', 'price', 'original_price',
            'cover_image', 'is_featured', 'is_bestseller', 'is_new',
            'average_rating', 'reviews_count', 'discount_percentage', 'stock_quantity'
        ]

class BookDetailSerializer(serializers.ModelSerializer):
    """Kitab detalları üçün tam serializer"""
    authors = AuthorSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    publisher = PublisherSerializer(read_only=True)
    reviews = BookReviewSerializer(many=True, read_only=True)
    average_rating = serializers.ReadOnlyField()
    reviews_count = serializers.ReadOnlyField()
    discount_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'slug', 'authors', 'category', 'publisher',
            'isbn', 'description', 'language', 'pages', 'publication_date',
            'price', 'original_price', 'stock_quantity',
            'cover_image', 'back_image',
            'is_featured', 'is_bestseller', 'is_new',
            'views_count', 'sales_count', 'created_at',
            'average_rating', 'reviews_count', 'discount_percentage', 'reviews'
        ]

from .models import Banner

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id', 'title', 'subtitle', 'image', 'link', 'is_active']

class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = [
            'site_name', 'site_description', 'phone', 'email', 
            'address', 'working_hours', 'copyright_year', 'facebook', 'instagram', 
            'twitter', 'youtube'
        ]
