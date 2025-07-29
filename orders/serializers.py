from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem
from books.serializers import BookListSerializer
from users.serializers import AddressSerializer

class CartItemSerializer(serializers.ModelSerializer):
    book = BookListSerializer(read_only=True)
    book_id = serializers.IntegerField(write_only=True)
    total_price = serializers.ReadOnlyField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'book', 'book_id', 'quantity', 'total_price', 'added_at']
        read_only_fields = ['id', 'added_at']

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
    delivery_address_id = serializers.IntegerField()
    
    class Meta:
        model = Order
        fields = [
            'delivery_address_id', 'delivery_name', 'delivery_phone', 
            'payment_method', 'notes'
        ]
    
    def create(self, validated_data):
        user = self.context['request'].user
        delivery_address_id = validated_data.pop('delivery_address_id')
        
        # İstifadəçinin səbətini al
        cart = Cart.objects.get(user=user)
        if not cart.items.exists():
            raise serializers.ValidationError("Səbət boşdur!")
        
        # Çatdırılma ünvanını yoxla
        try:
            delivery_address = user.addresses.get(id=delivery_address_id, is_active=True)
        except:
            raise serializers.ValidationError("Çatdırılma ünvanı tapılmadı!")
        
        # Sifarişi yarat
        order = Order.objects.create(
            user=user,
            delivery_address=delivery_address,
            delivery_address_text=delivery_address.full_address,
            subtotal=cart.total_price,
            total_amount=cart.total_price,  # Hələlik çatdırılma pulsuz
            **validated_data
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
