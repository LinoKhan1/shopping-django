# imports
from django import forms
from .models import Account, UserProfile


# User Registration Form
class RegistrationForm(forms.ModelForm):

    # Giving a placeholder and class to the password fields(register template)
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'enter password',
        'class': 'form-control'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'confirm password',
    }))

    # class Meta to define which fields to display in form from the Account model
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    # __init_ function used to set the placeholder and class of the form's fields and assign
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    # function to check if the passwords match
    def clean(self):
        # returns a dictionary of validated form input fields and their values
        cleaned_data = super(RegistrationForm, self).clean()
        # storing the values from the form's input fields into variables
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        # checking the passwords match, raise an error if they don't
        if password != confirm_password:
            raise forms.ValidationError(
                'Password does not match!'
            )


# User Form
class UserForm(forms.ModelForm):

    # class Meta to define which fields to display in form from the Account model
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number')

    # __init__ function used to give a class to the input fields
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


# User Profile Form
class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages={'invalid': "Images files only"},
                                     widget=forms.FileInput)

    # class Meta to define which fields to display in form from the User Profile model
    class Meta:
        model = UserProfile
        fields = ('address_line_1', 'address_line_2', 'city', 'state', 'country', 'profile_picture')

    # __init__ function used to give a class to the input fields
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

