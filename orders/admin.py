from django.contrib import admin
from django.utils.html import format_html
from .models import Cart, CartItem, Order, OrderItem, OrderStatusHistory

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['added_at', 'total_price']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_items', 'total_price', 'updated_at']
    search_fields = ['user__username', 'user__email']
    inlines = [CartItemInline]
    readonly_fields = ['total_items', 'total_price']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['total_price']

class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ['created_at', 'created_by']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_number', 'user', 'status', 'payment_status', 
        'total_amount', 'created_at'
    ]
    list_filter = [
        'status', 'payment_status', 'payment_method', 'created_at'
    ]
    search_fields = [
        'order_number', 'user__username', 'user__email', 
        'delivery_name', 'delivery_phone'
    ]
    list_editable = ['status', 'payment_status']
    inlines = [OrderItemInline, OrderStatusHistoryInline]
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Sifariş Məlumatları', {
            'fields': ('order_number', 'user', 'status', 'payment_status', 'payment_method')
        }),
        ('Qiymət Məlumatları', {
            'fields': ('subtotal', 'shipping_cost', 'discount_amount', 'total_amount')
        }),
        ('Çatdırılma Məlumatları', {
            'fields': ('delivery_name', 'delivery_phone', 'delivery_address', 'delivery_address_text')
        }),
        ('Qeydlər', {
            'fields': ('notes', 'admin_notes')
        }),
        ('Tarixlər', {
            'fields': ('created_at', 'updated_at', 'shipped_at', 'delivered_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if change:
            # Status dəyişikliyi tarixçəyə əlavə et
            old_obj = Order.objects.get(pk=obj.pk)
            if old_obj.status != obj.status:
                OrderStatusHistory.objects.create(
                    order=obj,
                    status=obj.status,
                    notes=f"Status dəyişdirildi: {old_obj.get_status_display()} → {obj.get_status_display()}",
                    created_by=request.user
                )
        super().save_model(request, obj, form, change)

@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ['order', 'status', 'created_at', 'created_by']
    list_filter = ['status', 'created_at']
    search_fields = ['order__order_number', 'notes']
    readonly_fields = ['created_at']
