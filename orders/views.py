from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem, Order
from books.models import Book
from .serializers import CartSerializer, CartItemSerializer, OrderSerializer, OrderCreateSerializer

class CartView(generics.RetrieveAPIView):
    """İstifadəçinin səbəti"""
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_to_cart(request):
    """Səbətə məhsul əlavə et"""
    book_id = request.data.get('book_id')
    quantity = int(request.data.get('quantity', 1))
    
    if not book_id:
        return Response({'error': 'Kitab ID tələb olunur!'}, status=status.HTTP_400_BAD_REQUEST)
    
    book = get_object_or_404(Book, id=book_id, is_active=True)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Stok yoxlaması
    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
    new_quantity = quantity if created else cart_item.quantity + quantity
    
    if new_quantity > book.stock_quantity:
        return Response({
            'error': f'Stokda yalnız {book.stock_quantity} ədəd var!'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    cart_item.quantity = new_quantity
    cart_item.save()
    
    return Response({
        'message': 'Məhsul səbətə əlavə edildi!',
        'cart': CartSerializer(cart).data
    })

@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_cart_item(request, item_id):
    """Səbət elementini yenilə"""
    quantity = int(request.data.get('quantity', 1))
    
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if quantity <= 0:
        cart_item.delete()
        return Response({'message': 'Məhsul səbətdən silindi!'})
    
    if quantity > cart_item.book.stock_quantity:
        return Response({
            'error': f'Stokda yalnız {cart_item.book.stock_quantity} ədəd var!'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    cart_item.quantity = quantity
    cart_item.save()
    
    return Response({
        'message': 'Səbət yeniləndi!',
        'cart': CartSerializer(cart_item.cart).data
    })

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def remove_from_cart(request, item_id):
    """Səbətdən məhsul sil"""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    
    return Response({'message': 'Məhsul səbətdən silindi!'})

class OrderListView(generics.ListAPIView):
    """İstifadəçinin sifarişləri"""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class OrderDetailView(generics.RetrieveAPIView):
    """Sifariş detalları"""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class OrderCreateView(generics.CreateAPIView):
    """Sifariş yarat"""
    serializer_class = OrderCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        
        return Response({
            'message': 'Sifariş uğurla yaradıldı!',
            'order': OrderSerializer(order).data
        }, status=status.HTTP_201_CREATED)
