from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm

class VendorRegForm(UserCreationForm):
    """The form for vendors to register their accounts."""
    fields = ('fullname', 'username', 'address', 'first_phone_number', 'second_phone_number')