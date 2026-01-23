from django.contrib import admin
from .models import Order, OrderLineItem

# Used AI to generate these admin views as Custom views
# will be required later anyway
class OrderLineItemInline(admin.TabularInline):
    """
    Inline admin for order line items to display within order admin
    """
    model = OrderLineItem
    readonly_fields = ('line_total',)
    fields = ('product', 'product_name', 'product_price', 'product_delivery', 'quantity', 'line_total')
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin view for Order model with inline line items
    """
    inlines = [OrderLineItemInline]
    
    readonly_fields = ('order_id', 'date', 'delivery_cost', 'order_total', 'grand_total')
    
    list_display = (
        'order_id',
        'date',
        'full_name',
        'email',
        'order_total',
        'delivery_cost',
        'grand_total',
        'is_paid',
    )
    
    list_filter = ('is_paid', 'date', 'country')
    
    search_fields = ('order_id', 'full_name', 'email', 'stripe_pid')
    
    ordering = ('-date',)
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_id', 'date', 'user', 'is_paid', 'stripe_pid')
        }),
        ('Customer Details', {
            'fields': ('full_name', 'email', 'phoneNumber')
        }),
        ('Delivery Address', {
            'fields': ('street_address1', 'street_address2', 'town_city', 'postcode', 'country')
        }),
        ('Order Totals', {
            'fields': ('order_total', 'delivery_cost', 'grand_total')
        }),
    )


@admin.register(OrderLineItem)
class OrderLineItemAdmin(admin.ModelAdmin):
    """
    Admin view for OrderLineItem model
    """
    list_display = (
        'order',
        'product_name',
        'quantity',
        'product_price',
        'line_total',
    )
    
    readonly_fields = ('line_total',)
    
    list_filter = ('order__date',)
    
    search_fields = ('order__order_id', 'product_name')
