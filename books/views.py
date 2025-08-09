from rest_framework import generics, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Category, Book, BookReview, Banner, SiteSettings
from .serializers import CategorySerializer, BookListSerializer, BookDetailSerializer, BookReviewSerializer, BannerSerializer, SiteSettingsSerializer
from .filters import BookFilter
from rest_framework import generics, filters, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListAPIView, RetrieveAPIView
from users.models import AnonymousUser
import uuid

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
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class BookDetailView(generics.RetrieveAPIView):
    """Kitab detalları"""
    queryset = Book.objects.filter(is_active=True).select_related('category', 'publisher').prefetch_related('authors', 'reviews__user')
    serializer_class = BookDetailSerializer
    lookup_field = 'slug'
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
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
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class BestsellerBooksView(generics.ListAPIView):
    """Bestseller kitablar"""
    queryset = Book.objects.filter(is_active=True, is_bestseller=True).select_related('category').prefetch_related('authors')
    serializer_class = BookListSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class NewBooksView(generics.ListAPIView):
    """Yeni kitablar"""
    queryset = Book.objects.filter(is_active=True, is_new=True).select_related('category').prefetch_related('authors')
    serializer_class = BookListSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class BookReviewListView(generics.ListCreateAPIView):
    """Kitab rəyləri"""
    serializer_class = BookReviewSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        book_id = self.kwargs.get('pk')
        return BookReview.objects.filter(book_id=book_id).select_related('user', 'anonymous_user')
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [AllowAny()]  # POST üçün də AllowAny
    
    def perform_create(self, serializer):
        book_id = self.kwargs.get('pk')
        book = Book.objects.get(id=book_id)
        
        # Anonymous user yaradır və ya mövcud olanı tapır
        device_id = self.request.META.get('HTTP_X_DEVICE_ID')
        if not device_id:
            device_id = str(uuid.uuid4())
        
        anonymous_user = AnonymousUser.get_or_create_anonymous(device_id)
        self.request.anonymous_user = anonymous_user
        
        review = serializer.save(book=book)
        return review
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.status_code = 201
        return response


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

class BannerListView(ListAPIView):
    queryset = Banner.objects.filter(is_active=True)
    serializer_class = BannerSerializer

class SiteSettingsView(RetrieveAPIView):
    """Sayt tənzimləmələri"""
    serializer_class = SiteSettingsSerializer
    permission_classes = [AllowAny]
    
    def get_object(self):
        return SiteSettings.get_settings()

@api_view(['GET'])
def whatsapp_number(request):
    """WhatsApp nömrəsini qaytarır"""
    settings = SiteSettings.get_settings()
    return Response({
        'whatsapp_number': settings.whatsapp_number
    })
