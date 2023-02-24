# Imports
from django.urls import path
from . import views

# urlpatterns, link to specific view from the view will render the html template
urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
    path('order_complete/', views.order_complete, name='order_complete'),
]