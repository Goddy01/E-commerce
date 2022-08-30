from django.shortcuts import render
from .forms import PaymentForm
from datetime import datetime
from django.contrib import messages

# def initiate_payment(request):
#     if request.method == 'POST':
#         payment_form = PaymentForm(request.POST)
#         if payment_form.is_valid():
#             payment = payment_form.save()
#             render(request, 'make_payment.html', {'payment': payment})
#         else:
#             payment_form = PaymentForm()
#     return render(request, 'initiate_payment.html', {'payment_form': payment_form})