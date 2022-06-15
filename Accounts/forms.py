from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth import authenticate
from .models import User_Acct

class RegForm(UserCreationForm):
    """The form for vendors to register their accounts."""
    email = forms.EmailField(max_length=128, help_text="Provide a valid email address.")
    class Meta:
        model = User_Acct
        fields = ['fullname', 'username', 'address', 'first_phone_num', 'second_phone_num', 'email','password1', 'password2']


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    class Meta:
        model = User_Acct
        fields = ['email', 'password']

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email'].lower()
            password = self.cleaned_data['password']
            user = authenticate(email=email, password=password)

            if not user:
                raise forms.ValidationError('Invalid login details')