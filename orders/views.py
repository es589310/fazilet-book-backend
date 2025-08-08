# orders/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from users.models import AnonymousUser
from books.models import Book
import uuid

class CartView(generics.RetrieveUpdateDestroyAPIView):
    """Səbət görüntüləmə və yeniləmə"""
    serializer_class = CartSerializer
    permission_classes = [AllowAny]
    
    def get_object(self):
        device_id = self.request.META.get('HTTP_X_DEVICE_ID', str(uuid.uuid4()))
        anonymous_user = AnonymousUser.get_or_create_anonymous(device_id)
        
        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
        else:
            cart = Cart.objects.filter(anonymous_user=anonymous_user).first()
            if not cart:
                cart = Cart.objects.create(anonymous_user=anonymous_user)
        
        return cart

class AddToCartView(generics.CreateAPIView):
    """Səbətə əlavə etmə"""
    serializer_class = CartItemSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        book = serializer.validated_data['book']  # artıq model obyekti
        quantity = serializer.validated_data.get('quantity', 1)
        
        if quantity > book.stock_quantity:
            return Response({
                'error': f'Stokda yalnız {book.stock_quantity} ədəd var!'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        device_id = self.request.META.get('HTTP_X_DEVICE_ID', str(uuid.uuid4()))
        anonymous_user = AnonymousUser.get_or_create_anonymous(device_id)
        
        
        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
        else:
            cart = Cart.objects.filter(anonymous_user=anonymous_user).first()
            if not cart:
                cart = Cart.objects.create(anonymous_user=anonymous_user)


        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            book=book,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return Response({
            'message': 'Kitab səbətə əlavə edildi',
            'cart_item_id': cart_item.id,
            'quantity': cart_item.quantity,
            'cart': CartSerializer(cart).data
        }, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([AllowAny])
def update_cart_item(request, item_id):
    """Səbət elementini yenilə"""
    quantity = int(request.data.get('quantity', 1))
    
    # Device ID-ni al
    device_id = request.META.get('HTTP_X_DEVICE_ID')
    if not device_id:
        device_id = str(uuid.uuid4())
    
    # Anonymous user yaradır və ya mövcud olanı tapır
    anonymous_user = AnonymousUser.get_or_create_anonymous(device_id)
    
    # Cart item-i tap
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    else:
        cart_item = get_object_or_404(CartItem, id=item_id, cart__anonymous_user=anonymous_user)
    
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
@permission_classes([AllowAny])
def remove_cart_item(request, item_id):
    """Səbətdən məhsul sil"""
    # Device ID-ni al
    device_id = request.META.get('HTTP_X_DEVICE_ID')
    if not device_id:
        device_id = str(uuid.uuid4())
    
    # Anonymous user yaradır və ya mövcud olanı tapır
    anonymous_user = AnonymousUser.get_or_create_anonymous(device_id)
    
    # Cart item-i tap
    if request.user.is_authenticated:
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    else:
        cart_item = get_object_or_404(CartItem, id=item_id, cart__anonymous_user=anonymous_user)
    
    cart_item.delete()
    
    return Response({'message': 'Məhsul səbətdən silindi!'})
