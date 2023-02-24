# imports
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Creating account's app models.

# Account Model
class MyAccountManager(BaseUserManager):

    # function used to create a normal user
    def create_user(self, first_name, last_name, username, email, password=None):
        # checking if the user has entered a valid email
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # function used to create a super_user (admin)
    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


# Custom User Model
class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=201)
    last_name = models.CharField(max_length=201)
    username = models.CharField(max_length=201, unique=True)
    email = models.EmailField(max_length=201, unique=True)
    phone_number = models.CharField(max_length=201)

    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_join = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    # to allow the user to log in with email instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    # function to combine the first and last name into a full_name
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    # String representation of the model
    def __str__(self):
        return self.email

    # functions used to give permission to the admin
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


# User Profile model
class UserProfile(models.Model):

    # Defining the attributes/fields of the model
    # Foreign Key referring to the user field in account model
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    address_line_1 = models.CharField(blank=True, max_length=100)
    address_line_2 = models.CharField(blank=True, max_length=100)
    profile_picture = models.ImageField(blank=True, max_length=255, upload_to='userprofile')
    city = models.CharField(blank=True, max_length=20)
    state = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)

    # String representation of the model
    def __str__(self):
        return self.user.first_name

    # Function to combine the two address lines into one full address
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'


