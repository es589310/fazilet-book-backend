from rest_framework import generics, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Category, Book, BookReview, Banner
from .serializers import CategorySerializer, BookListSerializer, BookDetailSerializer, BookReviewSerializer, BannerSerializer
from .filters import BookFilter
from rest_framework import generics, filters, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from users.models import AnonymousUser
import uuid
import logging

# Production logging
logger = logging.getLogger(__name__)

# Production rate limiting
class BookReviewThrottle(UserRateThrottle):
    rate = '10/hour'  # Authenticated users: 10 requests per hour

class BookReviewAnonThrottle(AnonRateThrottle):
    rate = '5/hour'   # Anonymous users: 5 requests per hour

class CategoryListView(generics.ListAPIView):
    """Kateqoriyalar siyahısı"""
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    throttle_classes = [AnonRateThrottle]

class BookListView(generics.ListAPIView):
    """Kitablar siyahısı"""
    queryset = Book.objects.filter(is_active=True).select_related('category', 'publisher').prefetch_related('authors')
    serializer_class = BookListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'authors__name', 'description']
    ordering_fields = ['price', 'created_at', 'sales_count', 'views_count']
    ordering = ['-created_at']
    throttle_classes = [AnonRateThrottle]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class BookDetailView(generics.RetrieveAPIView):
    """Kitab detalları"""
    queryset = Book.objects.filter(is_active=True).select_related('category', 'publisher').prefetch_related('authors', 'reviews__user')
    serializer_class = BookDetailSerializer
    lookup_field = 'slug'
    throttle_classes = [AnonRateThrottle]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            # Baxış sayını artır
            instance.views_count += 1
            instance.save(update_fields=['views_count'])
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Book detail error: {str(e)}")
            return Response({
                'success': False,
                'error': 'Kitab məlumatları yüklənə bilmədi'
            }, status=500)

class FeaturedBooksView(generics.ListAPIView):
    """Seçilmiş kitablar"""
    queryset = Book.objects.filter(is_active=True, is_featured=True).select_related('category').prefetch_related('authors')
    serializer_class = BookListSerializer
    throttle_classes = [AnonRateThrottle]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class BestsellerBooksView(generics.ListAPIView):
    """Bestseller kitablar"""
    queryset = Book.objects.filter(is_active=True, is_bestseller=True).select_related('category').prefetch_related('authors')
    serializer_class = BookListSerializer
    throttle_classes = [AnonRateThrottle]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class NewBooksView(generics.ListAPIView):
    """Yeni kitablar"""
    queryset = Book.objects.filter(is_active=True, is_new=True).select_related('category').prefetch_related('authors')
    serializer_class = BookListSerializer
    throttle_classes = [AnonRateThrottle]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class BookReviewListView(generics.ListCreateAPIView):
    """Kitab rəyləri - Production Security ilə"""
    serializer_class = BookReviewSerializer
    permission_classes = [AllowAny]
    throttle_classes = [BookReviewThrottle, BookReviewAnonThrottle]
    
    def get_queryset(self):
        book_id = self.kwargs.get('pk')
        return BookReview.objects.filter(book_id=book_id).select_related('user', 'anonymous_user')
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [AllowAny()]  # POST üçün də AllowAny (rate limiting ilə qorunur)
    
    def perform_create(self, serializer):
        try:
            book_id = self.kwargs.get('pk')
            book = Book.objects.get(id=book_id)
            
            # Anonymous user yaradır və ya mövcud olanı tapır
            device_id = self.request.META.get('HTTP_X_DEVICE_ID')
            if not device_id:
                device_id = str(uuid.uuid4())
            
            anonymous_user = AnonymousUser.get_or_create_anonymous(device_id)
            self.request.anonymous_user = anonymous_user
            
            review = serializer.save(book=book)
            
            # Production logging
            logger.info(f"Book review created: Book ID {book_id}, Rating {review.rating}")
            
            return review
            
        except ObjectDoesNotExist:
            logger.error(f"Book not found for review: Book ID {book_id}")
            raise ValidationError('Kitab tapılmadı')
        except Exception as e:
            logger.error(f"Review creation error: {str(e)}")
            raise ValidationError('Rəy yaradıla bilmədi')
    
    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            response.status_code = 201
            return response
        except Exception as e:
            logger.error(f"Review creation error: {str(e)}")
            return Response({
                'success': False,
                'error': 'Rəy yaradıla bilmədi'
            }, status=500)

@api_view(['GET'])
def book_stats(request):
    """Kitab statistikaları - Production Error Handling ilə"""
    try:
        total_books = Book.objects.filter(is_active=True).count()
        featured_books = Book.objects.filter(is_active=True, is_featured=True).count()
        bestsellers = Book.objects.filter(is_active=True, is_bestseller=True).count()
        new_books = Book.objects.filter(is_active=True, is_new=True).count()
        
        return Response({
            'success': True,
            'total_books': total_books,
            'featured_books': featured_books,
            'bestsellers': bestsellers,
            'new_books': new_books,
        })
    except Exception as e:
        logger.error(f"Book stats error: {str(e)}")
        return Response({
            'success': False,
            'error': 'Statistika məlumatları yüklənə bilmədi'
        }, status=500)

class BannerListView(ListAPIView):
    """Banner siyahısı - Production Security ilə"""
    queryset = Banner.objects.filter(is_active=True)
    serializer_class = BannerSerializer
    throttle_classes = [AnonRateThrottle]

@api_view(['POST'])
def upload_image_to_imagekit(request):
    """Şəkli ImageKit-ə yükləyir - Production Error Handling ilə"""
    try:
        # Production validation
        if 'image' not in request.FILES:
            return Response({
                'success': False,
                'error': 'Şəkil faylı tələb olunur'
            }, status=400)
        
        image_file = request.FILES['image']
        
        # File size validation (5MB limit)
        if image_file.size > 5 * 1024 * 1024:
            return Response({
                'success': False,
                'error': 'Şəkil faylının ölçüsü 5MB-dan çox ola bilməz'
            }, status=400)
        
        # File type validation
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
        if image_file.content_type not in allowed_types:
            return Response({
                'success': False,
                'error': 'Yalnız JPEG, PNG və WebP formatları dəstəklənir'
            }, status=400)
        
        folder_path = request.POST.get('folder', 'general')
        filename = request.POST.get('filename', None)
        
        # Production ImageKit handling
        try:
            from lib.imagekit_utils import imagekit_manager
            result = imagekit_manager.upload_image(
                image_file, 
                folder_path=folder_path,
                filename=filename
            )
            
            if result['success']:
                logger.info(f"Image uploaded successfully: {result['filename']}")
                return Response({
                    'success': True,
                    'url': result['url'],
                    'file_id': result['file_id'],
                    'filename': result['filename'],
                    'size': result['size'],
                    'width': result['width'],
                    'height': result['height']
                })
            else:
                logger.error(f"ImageKit upload failed: {result['error']}")
                return Response({
                    'success': False,
                    'error': 'Şəkil yüklənmədi'
                }, status=500)
                
        except ImportError:
            # ImageKit not available - fallback to local storage
            logger.warning("ImageKit not available, using local storage")
            return Response({
                'success': False,
                'error': 'Şəkil yükləmə xidməti müvəqqəti olaraq əlçatan deyil'
            }, status=503)
            
    except Exception as e:
        # Production error logging (no sensitive info)
        logger.error(f"Image upload error: {str(e)}")
        return Response({
            'success': False,
            'error': 'Şəkil yüklənmədi'
        }, status=500)
