# Imports
from django.contrib import admin
from .models import Carts, CartItem


# Cart Admin class, defining how to display fields in the model
class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_added')


# Cart Item Admin class, defining how to display fields in the model
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart', 'quantity', 'is_active')


# Registering the models
admin.site.register(Carts, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
