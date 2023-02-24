# Imports
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from store.models import Product, Variation
from carts.models import Carts, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


# Creating the app's views
# getting the cart_id from the session
def _cart_id(request):
    cart = request.session.session_key
    # if not, create a new session
    if not cart:
        cart = request.session.create()
    return cart


# Add Cart View to add items in the cart
def add_cart(request, product_id):
    # getting the current user
    current_user = request.user
    # Getting the product data from the product model
    product = Product.objects.get(id=product_id)
    # checking if the user is authenticated
    if current_user.is_authenticated:
        # assigning product variation to an empty list
        product_variation = []
        # checking form method == POST
        if request.method == 'POST':

            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key,
                                                      variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass
        # checking if cart_items exist within the above cart
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()

        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            # existing variation
            ex_var_list = []
            # item_id
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            print(ex_var_list)
            # checking if the product already exists
            # increase quantity if true else create new cart_item
            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                # create a new cart item
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variation.clear()
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=current_user,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('carts')

    # If the user is not authenticated
    else:
        # assigning product variation to an empty list
        product_variation = []

        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key,
                                                      variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass
        try:
            # get the cart using the cart_id present in the session
            cart = Carts.objects.get(cart_id=_cart_id(request))
        except Carts.DoesNotExist:
            # create cart if cart_id does not exists
            cart = Carts.objects.create(
                cart_id=_cart_id(request)
            )
        # saving the cart
        cart.save()

        # checking if cart_items exist within the above cart
        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()

        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, cart=cart)
            # existing variation --> database
            # current variation --> product_variation
            # item_id --> database
            ex_var_list = []
            id = []
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            print(ex_var_list)

            # checking if the product already exists
            # increase quantity if true else create new cart_item
            if product_variation in ex_var_list:
                # increase cart_item quantity

                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('carts')


# Remove Cart View, removing item from the cart
def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)

    try:
        # retrieving cart_item for an authenticated user
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        # retrieving cart_item for user who isn't authenticated
        else:
            cart = Carts.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        # if the item quantity  > 1 remove on item from the cart_item else delete item from the cart
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('carts')


# Remove Cart Item, removing cart_item from the cart
def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Carts.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('carts')


# Cart View
def carts(request, total=0, quantity=0, cart_items=None):

    # initializing tax and grand_total variables
    tax = 0
    grand_total = 0

    try:
        # For authenticated users
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        # For not authenticated users
        else:
            cart = Carts.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        # looping through the cart_items
        # Calculating the total, tax, and grand_total
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }
    return render(request, 'store/carts.html', context)


# Checkout View, retrieve cart data, to be displayed on the checkout template
# Code similar to the cart view
@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Carts.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }
    return render(request, 'store/checkout.html', context)