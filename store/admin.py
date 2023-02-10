from django.contrib import admin
from .models import Product

# Class to pre-populate the slug


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}

# Register your models here.


admin.site.register(Product, ProductAdmin)
