# Imports
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Product, Category, ReviewRating
from orders.models import OrderProduct
from .models import ProductGallery
from carts.views import CartItem, _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .forms import ReviewForm
from django.contrib import messages


# Creating app's views.
# Store View
def store(request, category_slug=None):
    categories = None
    products = None
    page_products = None
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        product_count = products.count()
    else:
        # Query to fetch all products that are available
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        page_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        'products': products,
        'page_products': page_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)

# Product Detail View
def product_detail(request, category_slug, product_slug):

    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except:
            orderproduct = None
    else:
        orderproduct = None

    # Getting the reviews
    reviews = ReviewRating.objects.filter(product_id=single_product.id,status=True)

    # Get the product gallery
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)


    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
        'product_gallery': product_gallery,
    }
    return render(request, 'store/product-detail.html', context)


# Search View, returning products from the db
# based on the keyword entered by the user
def search(request):

    # Initializing the product count
    product_count = 0
    # Checking if the keyword name is in the get request
    if 'keyword' in request.GET:
        # Store the keyword
        keyword = request.GET['keyword']
        # If true search the in the db (product_name & description)
        # If contains keyword return the product
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) |
                                                                        Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,

    }

    return render(request, 'store/store.html', context)


# Submit Review View
def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, "Thank you! Your review has been updated")
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, "Thank you! Your review has been submitted")
                return redirect(url)



