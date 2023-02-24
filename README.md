E-Commerce Web Application (Python/Django)

Description:

Sample E-commerce web application that enables user to register, view store, add product
to the shopping cart, proceed to checkout and make payment.

The project contains different django applications including accounts, store, carts and others,
templates and static folders containng the html templates, css and js files

Languages, Tools & Framework:

- Python
- Django

Functionalities:

1.	Accounts

  •	User Account Registration
  
  •	Create User Profile after successful registration
  
  •	Email Verification and Account Activation
  
  •	Prevent the user from logging in if the account is not verified.
  
  •	Use Login
  
  •	User Logout/Logout after 1 hour of inactivity
  
  •	Forgot Password, enables the user to enter the email address and send a reset password link to the user’s mail address.
  
  •	Account Dashboard
  
      o	View Orders
      
      o	View Oder Details
      
      o	Edit Profile
      
      o	Change Password
      
2.	Store

  •	View store
  
  •	Search option
  
  •	Filter by product category
  
  •	View the product detail page.
  
  •	submit a rating for a bought product (the user must be authenticated and had purchased the product)

3.	Cart

  •	Add the product to the shopping cart with the production variation including the color and the size
  
  •	View the cart, displaying the product name, variation, price and quantity, subtotal, tax, and grand total.
  
  •	Increase/decrease the quantity of cart items.
  
  •	Delete cart items.
  
  •	Proceed to checkout.
  
  •	Prevent the user to proceed if not authenticated.
  
  •	Redirect the user to the checkout page after authentication.

4.	Orders

  •	Place Order
  
  •	Make payment (PayPal sandbox accounts for testing)
  
  •	Order Complete Invoice and Email
  
  •	Decrease the quantity of product in the model after payment

Contact
- Lino Khan: linokhan1@gmail.com
- Repository link: https://github.com/LinoKhan1/shopping-django.git






