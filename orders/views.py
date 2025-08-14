# orders/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem, Order, OrderItem
from .serializers import CartSerializer, CartItemSerializer, OrderCreateSerializer
from users.models import AnonymousUser, Address
from books.models import Book
import uuid
from rest_framework import serializers

class CartView(generics.RetrieveUpdateDestroyAPIView):
    """Səbət görüntüləmə və yeniləmə"""
    serializer_class = CartSerializer
    permission_classes = [AllowAny]
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
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
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
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

@api_view(['DELETE'])
@permission_classes([AllowAny])
def clear_cart(request):
    """Səbəti tamamilə təmizlə"""
    # Device ID-ni al
    device_id = request.META.get('HTTP_X_DEVICE_ID')
    if not device_id:
        device_id = str(uuid.uuid4())
    
    # Anonymous user yaradır və ya mövcud olanı tapır
    anonymous_user = AnonymousUser.get_or_create_anonymous(device_id)
    
    # Cart-i tap və bütün item-ləri sil
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        cart = Cart.objects.filter(anonymous_user=anonymous_user).first()
    
    if cart:
        cart.items.all().delete()
        return Response({'message': 'Səbət təmizləndi!'})
    
    return Response({'message': 'Səbət artıq boşdur!'})

@api_view(['POST'])
@permission_classes([AllowAny])
def create_order(request):
    """Sifariş yarat - həm profil olan, həm də anonim istifadəçilər üçün"""
    try:
        # Device ID-ni al
        device_id = request.META.get('HTTP_X_DEVICE_ID', str(uuid.uuid4()))
        anonymous_user = AnonymousUser.get_or_create_anonymous(device_id)
        
        # İstifadəçi məlumatlarını al
        user = request.user if request.user.is_authenticated else None
        
        # Səbəti tap
        if user:
            cart = Cart.objects.filter(user=user).first()
        else:
            cart = Cart.objects.filter(anonymous_user=anonymous_user).first()
        
        if not cart or not cart.items.exists():
            raise serializers.ValidationError("Səbət boşdur!")
        
        # Sifariş məlumatlarını yoxla
        delivery_name = request.data.get('delivery_name')
        delivery_phone = request.data.get('delivery_phone')
        delivery_address_text = request.data.get('delivery_address_text')
        payment_method = request.data.get('payment_method', 'cash')
        notes = request.data.get('notes', '')
        
        if not delivery_name or not delivery_phone or not delivery_address_text:
            raise serializers.ValidationError("Çatdırılma məlumatları tam deyil!")
        
        # Sifarişi yarat
        order = Order.objects.create(
            user=user,
            delivery_name=delivery_name,
            delivery_phone=delivery_phone,
            delivery_address_text=delivery_address_text,
            payment_method=payment_method,
            notes=notes,
            subtotal=cart.total_price,
            total_amount=cart.total_price,  # Hələlik çatdırılma pulsuz
            status='pending',
            payment_status='pending'
        )
        
        # Sifariş status tarixçəsi yarat
        from .models import OrderStatusHistory
        OrderStatusHistory.objects.create(
            order=order,
            status='pending',
            notes='Sifariş yaradıldı',
            created_by=user
        )
        
        # Səbət elementlərini sifarişə köçür
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                book=cart_item.book,
                quantity=cart_item.quantity,
                price=cart_item.book.price
            )
            
            # Kitabın satış sayını artır və stokunu azalt
            cart_item.book.sales_count += cart_item.quantity
            cart_item.book.stock_quantity -= cart_item.quantity
            cart_item.book.save()
        
        # Səbəti təmizlə
        cart.items.all().delete()
        
        # Sifariş məlumatlarını qaytar
        from .serializers import OrderSerializer
        order_data = OrderSerializer(order).data
        
        return Response({
            'message': 'Sifariş uğurla yaradıldı!',
            'order': order_data
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
