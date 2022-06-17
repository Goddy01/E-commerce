from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth import authenticate
from .models import Customer, Vendor, User_Acct

class CustomerRegForm(UserCreationForm):
    """The form for Customers to register their accounts."""
    email = forms.EmailField(max_length=128, help_text="Provide a valid email address.")
    class Meta:
        model = Customer
        fields = ['fullname', 'username', 'address', 'first_phone_num', 'second_phone_num', 'email','password1', 'password2']


# class CustomerLoginForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput, label='Password')
#     class Meta:
#         model = Customer
#         fields = ['email', 'password']

#     def clean(self):
#         if self.is_valid():
#             email = self.cleaned_data['email'].lower()
#             password = self.cleaned_data['password']
#             user = authenticate(email=email, password=password)

#             if not user:
#                 raise forms.ValidationError('Invalid login details')
class VendorRegForm(UserCreationForm):
    """The form for Customers to register their accounts."""
    email = forms.EmailField(max_length=128, help_text="Provide a valid email address.")
    class Meta:
        model = Vendor
        fields = ['fullname', 'username', 'address', 'first_phone_num', 'second_phone_num', 'email','password1', 'password2']


class CustomerLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    class Meta:
        model = Customer
        fields = ['email', 'password']

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email'].lower()
            password = self.cleaned_data['password']
            user = authenticate(email=email, password=password)

            if not user:
                raise forms.ValidationError('Invalid login details')

class VendorLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    class Meta:
        model = Vendor
        fields = ['email', 'password']

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email'].lower()
            password = self.cleaned_data['password']
            user = authenticate(email=email, password=password)

            if not user:
                raise forms.ValidationError('Invalid login details')