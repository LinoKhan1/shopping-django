# Imports
from django import forms
from .models import ReviewRating


# Review Form
class ReviewForm(forms.ModelForm):

    # Class Meta, define form fields
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']