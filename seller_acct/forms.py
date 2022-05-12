from xml.dom import ValidationErr
from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth import authenticate
from .models import Vendor_Acct

class VendorRegForm(UserCreationForm):
    """The form for vendors to register their accounts."""
    email = forms.EmailField(max_length=128, help_text="Provide a valid email address.")
    class Meta:
        model = Vendor_Acct
        fields = ('fullname', 'username', 'address', 'first_phone_num', 'second_phone_num', 'email')


class VendorLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    class Meta:
        model = Vendor_Acct
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data.get('email').lower()
            password = self.cleaned_data.get('password')
            user = authenticate(email=email, password=password)

            if not user:
                raise forms.ValidationError('Invalid login details')