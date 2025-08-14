# orders/serializers.py
from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem
from books.serializers import BookListSerializer
from users.serializers import AddressSerializer
from books.models import Book

class CartItemSerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(),
        source='book',
        write_only=True
    )
    total_price = serializers.ReadOnlyField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'book', 'book_id', 'quantity', 'total_price', 'added_at']
        read_only_fields = ['id', 'added_at']
    
    def get_book(self, obj):
        return BookListSerializer(obj.book, context=self.context).data
    
    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Miqdar 1-dən az ola bilməz")
        return value

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField()
    total_items = serializers.ReadOnlyField()
    
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price', 'total_items', 'updated_at']
        read_only_fields = ['id', 'updated_at']


class OrderItemSerializer(serializers.ModelSerializer):
    book = BookListSerializer(read_only=True)
    total_price = serializers.ReadOnlyField()
    
    class Meta:
        model = OrderItem
        fields = ['id', 'book', 'quantity', 'price', 'total_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    delivery_address = AddressSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'status', 'status_display', 
            'payment_status', 'payment_status_display', 'payment_method',
            'subtotal', 'shipping_cost', 'discount_amount', 'total_amount',
            'delivery_name', 'delivery_phone', 'delivery_address', 'delivery_address_text',
            'notes', 'created_at', 'items'
        ]
        read_only_fields = ['id', 'order_number', 'created_at']

class OrderCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = [
            'delivery_name', 'delivery_phone', 'delivery_address_text', 
            'payment_method', 'notes'
        ]
    
    def create(self, validated_data):
        user = self.context['request'].user
        
        # İstifadəçinin səbətini al
        cart = Cart.objects.get(user=user)
        if not cart.items.exists():
            raise serializers.ValidationError("Səbət boşdur!")
        
        # Sifarişi yarat
        order = Order.objects.create(
            user=user,
            delivery_address_text=validated_data.get('delivery_address_text', ''),
            subtotal=cart.total_price,
            total_amount=cart.total_price,  # Hələlik çatdırılma pulsuz
            **validated_data
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
        
        return order
