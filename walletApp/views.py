from django.shortcuts import render
from .forms import PaymentForm
from datetime import datetime
from django.contrib import messages
from django.conf import settings
from django.http import HttpRequest, HttpResponse

def initiate_payment(request: HttpRequest, amount, email) -> HttpResponse:
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            payment = payment_form.save(commit=False)
            payment.amount = amount
            payment.email = email
            payment.save()
            render(request, 'store/checkout.html', {'payment': payment, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})
        else:
            messages.error(request, 'Payment Failed!')
    else:
        payment_form = PaymentForm()
    return render(request, 'store/checkout.html', {'payment_form': payment_form})