from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from datetime import datetime
from django.contrib import messages
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from store.models import BillingAddress, Order

def make_payment(request):
    order = Order.objects.filter(customer__email=request.user.email).order_by('-id').first()
    return render(request, 'make_payment.html', {'total':order.total_order_price, 'email': order.customer.email})