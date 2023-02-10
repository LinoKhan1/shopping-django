from django.db import models
from django.urls import reverse

# Create your models here.

# Creating a class for the category
# Attributes representing fields in the database


class Category(models.Model):
    category_name = models.CharField(max_length=201, unique=True)
    # link to category
    slug = models.SlugField(max_length=201, unique=True)
    description = models.TextField(blank=True)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    # String Representation
    def __str__(self):
        return self.category_name
