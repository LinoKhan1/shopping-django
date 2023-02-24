# Imports
from django.db import models
from category.models import Category
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg, Count

# Creating app's models

# Product Model
class Product(models.Model):
    # Attributes/fields
    product_name = models.CharField(max_length=201, unique=True)
    slug = models.SlugField(max_length=201, unique=True)
    description = models.TextField(max_length=201, unique=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    # Getting the product url
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    # String representation of the model
    def __str__(self):
        return self.product_name
    # Getting the average review of the product
    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregrate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg
    # Counting the number of reviews
    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregrate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count


# Variation Manager, defining the product variation
# This case, color and size
class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active= True)
    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active = True)

variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),

)

# Variation Model
class Variation(models.Model):
    # Attributes/fields
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    # String representation of the model
    def __str__(self):
        return self.variation_value

# Review Ratig Model
class ReviewRating(models.Model):
    # Attributes/fields
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    # String representation of the model
    def __str__(self):
        return self.subject

# Product Gallery Model, storing different images of the product
class ProductGallery(models.Model):
    # Attributes/fields
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products', max_length=255)

    # String representation of the model
    def __str__(self):
        return self.product.product_name

    # Class Meta, defining the grammar for the model name in the db
    # Singular and plural form
    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'
