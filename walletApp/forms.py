from django import forms
from .models import Payment

class PaymentForn(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('payment', )