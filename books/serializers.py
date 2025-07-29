from rest_framework import serializers
from .models import Category, Author, Publisher, Book, BookReview

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'biography', 'birth_date', 'death_date', 'photo', 'nationality']

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'address', 'phone', 'email', 'website']

class BookReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = BookReview
        fields = ['id', 'user', 'user_name', 'rating', 'comment', 'created_at']
        read_only_fields = ['user']

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
