# imports
from django.contrib import admin
from .models import Product, Variation, ReviewRating, ProductGallery
import admin_thumbnails


# Adding the product gallery as an extra field in the product model
@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1


# Product Admin
class ProductAdmin(admin.ModelAdmin):
    # fields to display
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    # pre-populate the product slug
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [ProductGalleryInline]


# Variation Admin, display fields in the product variation model
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active', )
    list_filter = ('product', 'variation_category', 'variation_value')


# registering the models
admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)
