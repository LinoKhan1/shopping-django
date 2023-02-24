# Imports
from django import forms
from .models import Order


# Order Form
class OrderForm(forms.ModelForm):

    # Class Meta, define form fields
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2',
                  'city', 'state', 'country', 'order_note']