from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from .models import Vendor_Acct

class VendorRegForm(UserCreationForm):
    """The form for vendors to register their accounts."""
    email = forms.EmailField(max_length=128, help_text="Provide a valid email address.")
    class Meta:
        model = Vendor_Acct
        fields = ('fullname', 'username', 'address', 'first_phone_num', 'second_phone_num', 'email')