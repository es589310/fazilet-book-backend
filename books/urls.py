from django.urls import path
from . import views
from .views import BookReviewListView

urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('', views.BookListView.as_view(), name='book-list'),
    path('featured/', views.FeaturedBooksView.as_view(), name='featured-books'),
    path('bestsellers/', views.BestsellerBooksView.as_view(), name='bestseller-books'),
    path('new/', views.NewBooksView.as_view(), name='new-books'),
    path('stats/', views.book_stats, name='book-stats'),
    path('banners/', views.BannerListView.as_view(), name='banner-list'),

    path('upload-image/', views.upload_image_to_imagekit, name='upload-image'),
    path('<int:pk>/reviews/', BookReviewListView.as_view(), name='book-reviews'),
    path('<slug:slug>/', views.BookDetailView.as_view(), name='book-detail'),
]