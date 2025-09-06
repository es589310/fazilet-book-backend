from django.contrib import admin
from django.utils.html import format_html
from .models import Cart, CartItem, Order, OrderItem, OrderStatusHistory

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['added_at', 'total_price']
    fields = ['book', 'quantity', 'total_price', 'added_at']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart_identifier', 'book', 'quantity', 'total_price', 'added_at']
    list_filter = ['added_at']
    search_fields = ['book__title', 'cart__user__username', 'cart__anonymous_user__display_name']
    readonly_fields = ['added_at', 'total_price']
    
    def cart_identifier(self, obj):
        if obj.cart.user:
            return f"İstifadəçi: {obj.cart.user.username}"
        elif obj.cart.anonymous_user:
            return f"Anonim: {obj.cart.anonymous_user.display_name}"
        return "Anonim Səbət"
    cart_identifier.short_description = "Səbət"

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user_identifier', 'total_items', 'total_price', 'updated_at']
    list_filter = ['updated_at']
    search_fields = ['user__username', 'user__email', 'anonymous_user__display_name']
    inlines = [CartItemInline]
    readonly_fields = ['total_items', 'total_price', 'user_identifier']
    list_per_page = 20
    ordering = ['-updated_at']
    date_hierarchy = 'updated_at'
    
    fieldsets = (
        ('İstifadəçi Məlumatları', {
            'fields': ('user', 'anonymous_user'),
            'description': 'Səbətin sahibi olan istifadəçi'
        }),
        ('Statistik Məlumatlar', {
            'fields': ('total_items', 'total_price'),
            'description': 'Səbətdəki məhsulların sayı və ümumi qiyməti (avtomatik hesablanır)'
        }),
    )
    
    def user_identifier(self, obj):
        if obj.user:
            return f"İstifadəçi: {obj.user.username}"
        elif obj.anonymous_user:
            return f"Anonim: {obj.anonymous_user.display_name}"
        return "Anonim Səbət"
    user_identifier.short_description = "İstifadəçi"

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
        'order_number', 'user', 'delivery_name', 'delivery_phone', 'status', 'payment_status', 
        'total_amount', 'created_at'
    ]
    list_filter = [
        'status', 'payment_status', 'payment_method', 'created_at'
    ]
    search_fields = [
        'order_number', 'user__username', 'user__email', 
        'delivery_name', 'delivery_phone', 'delivery_address_text'
    ]
    list_editable = ['status', 'payment_status']
    inlines = [OrderItemInline, OrderStatusHistoryInline]
    readonly_fields = ['order_number', 'created_at', 'updated_at', 'subtotal', 'total_amount']
    list_per_page = 25
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Sifariş Məlumatları', {
            'fields': ('order_number', 'user', 'status', 'payment_status', 'payment_method'),
            'description': 'Sifarişin əsas məlumatları və statusu'
        }),
        ('Qiymət Məlumatları', {
            'fields': ('subtotal', 'shipping_cost', 'discount_amount', 'total_amount'),
            'description': 'Sifarişin qiymət hesablamaları'
        }),
        ('Çatdırılma Məlumatları', {
            'fields': ('delivery_name', 'delivery_phone', 'delivery_address_text'),
            'description': 'Məhsulun çatdırılması üçün lazım olan məlumatlar'
        }),
        ('Qeydlər', {
            'fields': ('notes', 'admin_notes'),
            'description': 'Sifariş haqqında əlavə qeydlər'
        }),
        ('Tarixlər', {
            'fields': ('created_at', 'updated_at', 'shipped_at', 'delivered_at'),
            'classes': ('collapse',),
            'description': 'Sifarişin müxtəlif mərhələlərdəki tarixləri'
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
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ['order', 'status', 'created_at', 'created_by']
    list_filter = ['status', 'created_at']
    search_fields = ['order__order_number', 'notes']
    readonly_fields = ['created_at']
