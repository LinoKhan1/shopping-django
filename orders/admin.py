# Imports
from django.contrib import admin
from .models import Payment, Order, OrderProduct
# Register your models here.


# Order Product Inline, specifying which are read only in the Order Product model
class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment', 'user', 'product', 'quantity', 'product_price', 'ordered')
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    # fields to display
    list_display = ['order_number', 'full_name', 'phone', 'email', 'city',
                    'order_total', 'tax', 'status', 'is_ordered', 'created_at']
    # filter by status and is_ordered
    list_filter = ['status', 'is_ordered']
    # search fields
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
    # number row per page
    list_per_page = 20
    inlines = [OrderProductInline]


# registering app's models
admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)



