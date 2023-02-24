# Imports
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm, UserForm , UserProfileForm
from .models import Account,UserProfile
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from carts.views import _cart_id
from carts.models import Carts, CartItem
from orders.models import Order, OrderProduct, Product
import requests

# verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage, send_mail

# Creating the account's app views


# Register View
def register(request):
    # checking if the submit button from the form was clicked and method == POST
    # else return the user to register template
    if request.method == 'POST':
        # storing form's input values into form dictionary
        form = RegistrationForm(request.POST)
        # checking if the form is valid
        if form.is_valid():
            # storing input values into variables
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name,
                                               email=email, username=username, password=password)
            user.phone_number = phone_number
            # saving the user info
            user.save()

            # Creating a user profile after successfully registration
            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_picture = 'default/default-user.png'
            profile.save()

            # USER ACTIVATION, sending activation link to the user mail address
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_mail(mail_subject,
                      message,
                      'balkhanol1@gmail.com',
                      [to_email],
                      fail_silently=False,)

            return redirect('/accounts/login/?command=verification&email=' + email)
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


# Login View
def login(request):
    # checking if the submit button was clicked and form method == POST
    if request.method == 'POST':
        # storing input values into variables
        email = request.POST['email']
        password = request.POST['password']

        # authenticate the user if the email and password provides match
        # the ones in the account model, else display an error message
        user = auth.authenticate(email=email, password=password)

        # if returns a user
        if user is not None:
            # Try except block for the production_variation/cart_items code
            # for an authenticated user, check add_cart view in the carts app
            try:
                # storing cart data for the authenticated user
                cart = Carts.objects.get(cart_id=_cart_id(request))

                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    # creating the product_variation by cart_id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    # Get the cart items from the user to access his product variations
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id(index)
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass

            auth.login(request, user)
            # This part is for the user who tried to access the checkout from the cart template
            # without being authenticated
            # sending the user log in template if not authenticated, once authenticated redirecting
            # to the checkout page
            url = request.META.get('HTTP_REFERER')
            # redirecting the user to the checkout page after he was prompted
            # to log in before checkout
            try:
                query = requests.utils.urlparse(url).query
                print('query->', query)
                print('------')
                # next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                print('params->', params)
                if 'next' in params:
                    next_page = params['next']
                    return redirect(next_page)
            except:
                return redirect('dashboard')
        else:
            # error message if the user provided invalid login credentials
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')


# Logout View
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out')
    return redirect('login')


# Activate View, to activate the user account
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated')
        return redirect('login')
    else:
        messages.error(request, 'Invalid Activation link')
        return redirect('register')


# Dashboard View
@login_required(login_url='login')
def dashboard(request):
    # retrieving data from order model for the authenticated user
    orders = Order.objects.order_by('created_at').filter(user_id=request.user.id, is_ordered=True)

    orders_count = orders.count()
    #userprofile = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'order_count': orders_count,
    }

    return render(request, 'accounts/dashboard.html', context)


# Forgot Password View
def forgot_password(request):
    # checking form method == POST
    if request.method == 'POST':
        # storing email input value into a variable
        email = request.POST['email']
        # checking if the email provided exists within the account model
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            # send reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset your password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_mail(mail_subject,
                      message,
                      'balkhanol1@gmailcom',
                      [to_email],
                      fail_silently=False,)

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            # error message if email does not exist within the model
            messages.error(request, 'Account does not exists')
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')


# Reset Password Validate View
def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link is expired')
        return redirect('login')


# Reset Password View
def reset_password(request):
    # checking if form method == POST
    if request.method == 'POST':
        # storing password's input values into variables
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        # checking if passwords match
        if password == confirm_password:
            # storing uid from the session
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            # set_password to set and hash password with the model
            user.set_password(password)
            # saving the new password
            user.save()
            # displaying a success message
            messages.success(request, 'Password reset successfully')
            return redirect('login')
        else:
            # error message if the passwords do not match
            messages.error(request, 'Password does not match')
            return redirect('reset_password')
    else:
        return render(request, 'accounts/reset_password.html')


# My Orders View, displaying orders from the authenticated user, in the dashboard (order template)
# login_required decorator, denying access if user is not authenticated
@login_required(login_url='login')
def my_orders(request):
    # retrieving data (authenticated user) from the order model
    # where is_ordered= True (meaning the user has paid)

    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    # Passing orders to the context dictionary to be displayed in the order template
    context = {
        'orders': orders,
    }
    # rendering the html page
    return render(request, 'accounts/my_orders.html', context)


# Edit Profile View, enabling the authenticated user to edit his/her profile
# login_required decorator, denying access if user is not authenticated

@login_required(login_url='login')
def edit_profile(request):
    # retrieving user profile data for the authenticated user
    # if not authenticated display 404 page does not exist error
    userprofile = get_object_or_404(UserProfile, user=request.user)
    # checking if form method == POST
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,

    }
    # rendering the html page
    return render(request, 'accounts/edit_profile.html', context)


# Change Password View, changing password from the account dashboard
# login_required decorator, denying access if user is not authenticated
@login_required(login_url='login')
def change_password(request):
    # checking if the form method == POST
    if request.method == 'POST':
        # storing password input values into variables
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_new_password']

        user = Account.objects.get(username__exact=request.user.username)
        # checking passwords match
        if new_password == confirm_password:
            # checking the current_password provided with the one in the db
            success = user.check_password(current_password)
            # if true, set and save new password, and display success message
            if success:
                user.set_password(new_password)
                user.save()

                messages.success(request, 'Password updated successfully')
                return redirect('change_password')
            else:
                # false, display an error message
                messages.error(request, 'Please enter valid current password')
                return redirect('change_password')
        else:
            # display error message (outer if condition)
            messages.error(request, 'Password does not match')
            return redirect('change_password')

    return render(request, 'accounts/change_password.html')


# Order Detail View, retrieving data of a specific order
# when clicked on the order_number in the order template
@login_required(login_url='login')
def order_detail(request, order_id):
    order_details = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_details:
        subtotal += i.product_price * i.quantity
    context = {
        'order_details': order_details,
        'order': order,
        'subtotal': subtotal
    }
    return render(request, 'accounts/order_detail.html', context)


