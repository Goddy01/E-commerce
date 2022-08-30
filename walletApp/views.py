from django.shortcuts import render, get_object_or_404, redirect
from .forms import PaymentForm
from .models import Payment
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
            return render(request, 'store/checkout.html', {'payment': payment, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})
        else:
            messages.error(request, 'Payment Failed!')
    else:
        payment_form = PaymentForm()
    return render(request, 'store/checkout.html', {'payment_form': payment_form})

def verify_payment(request: HttpRequest, ref: str) -> HttpResponse:
    trxref = request.GET["trxref"]
    if trxref != ref:
        messages.error(
            request,
            "The transaction reference passed was different from the actual reference. Please do not modify data during transactions",
        )
    payment: Payment = get_object_or_404(Payment, ref=ref)
    if payment.verify_payment():
        messages.success(
            request, f"Payment Completed Successfully, NGN #{payment.amount}."
        )
        messages.success(
            request, f"Your new credit balance is GH₵ {payment.user.credit}."
        )
    else:
        messages.warning(request, "Sorry, your payment could not be confirmed.")
    return redirect("initiate-payment")