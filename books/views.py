from rest_framework import generics, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Category, Book, BookReview
from .serializers import CategorySerializer, BookListSerializer, BookDetailSerializer, BookReviewSerializer
from .filters import BookFilter

class CategoryListView(generics.ListAPIView):
    """Kateqoriyalar siyahısı"""
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer

class BookListView(generics.ListAPIView):
    """Kitablar siyahısı"""
    queryset = Book.objects.filter(is_active=True).select_related('category', 'publisher').prefetch_related('authors')
    serializer_class = BookListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'authors__name', 'description']
    ordering_fields = ['price', 'created_at', 'sales_count', 'views_count']
    ordering = ['-created_at']

class BookDetailView(generics.RetrieveAPIView):
    """Kitab detalları"""
    queryset = Book.objects.filter(is_active=True).select_related('category', 'publisher').prefetch_related('authors', 'reviews__user')
    serializer_class = BookDetailSerializer
    lookup_field = 'slug'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Baxış sayını artır
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class FeaturedBooksView(generics.ListAPIView):
    """Seçilmiş kitablar"""
    queryset = Book.objects.filter(is_active=True, is_featured=True).select_related('category').prefetch_related('authors')
    serializer_class = BookListSerializer

class BestsellerBooksView(generics.ListAPIView):
    """Bestseller kitablar"""
    queryset = Book.objects.filter(is_active=True, is_bestseller=True).select_related('category').prefetch_related('authors')
    serializer_class = BookListSerializer

class NewBooksView(generics.ListAPIView):
    """Yeni kitablar"""
    queryset = Book.objects.filter(is_active=True, is_new=True).select_related('category').prefetch_related('authors')
    serializer_class = BookListSerializer

@api_view(['GET'])
def book_stats(request):
    """Kitab statistikaları"""
    total_books = Book.objects.filter(is_active=True).count()
    featured_books = Book.objects.filter(is_active=True, is_featured=True).count()
    bestsellers = Book.objects.filter(is_active=True, is_bestseller=True).count()
    new_books = Book.objects.filter(is_active=True, is_new=True).count()
    
    return Response({
        'total_books': total_books,
        'featured_books': featured_books,
        'bestsellers': bestsellers,
        'new_books': new_books,
    })
