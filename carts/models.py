from django.db import models
from store.models import Product, Variation
from accounts.models import Account


# Create your models here.


class Carts(models.Model):
    cart_id = models.CharField(max_length=201, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    #variation = models.ManyToManyField(Variation, blank=True) testing if varation(s) was the issue
    cart = models.ForeignKey(Carts, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.product

