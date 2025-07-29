import django_filters
from .models import Book, Category

class BookFilter(django_filters.FilterSet):
    """Kitab filtri"""
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.filter(is_active=True))
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    language = django_filters.ChoiceFilter(choices=Book.LANGUAGE_CHOICES)
    is_featured = django_filters.BooleanFilter()
    is_bestseller = django_filters.BooleanFilter()
    is_new = django_filters.BooleanFilter()
    
    class Meta:
        model = Book
        fields = ['category', 'language', 'is_featured', 'is_bestseller', 'is_new']
