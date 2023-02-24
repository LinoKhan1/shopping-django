# Imports
from django.db import models
from store.models import Product, Variation
from accounts.models import Account


# Creating cart's app model
class Carts(models.Model):
    # attributes/fields of the Carts model
    cart_id = models.CharField(max_length=201, blank=True)
    date_added = models.DateField(auto_now_add=True)

    # String representation of the model
    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    # attributes/fields of the Carts model
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Carts, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    # sub_total function to calculate the subtotal of the cart items
    def sub_total(self):
        return self.product.price * self.quantity

    # render an object in the context where the string representation is needed
    def __unicode__(self):
        return self.product

