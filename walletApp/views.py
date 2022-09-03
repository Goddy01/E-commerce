from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from datetime import datetime
from django.contrib import messages
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from store.models import BillingAddress, Order

def make_payment(request):
    order = Order.objects.filter(customer__email=request.user.email).order_by('-id').first()
    request.session['total'] = order.total_order_price
    request.session['email'] = request.user.email
    if request.session.get('total') == order.total_order_price:
        order.complete = not order.complete
    order.save()
    # email = order.customer.email
    return render(request, 'make_payment.html', {'total': request.session.get('total'), 'email': request.session.get('email')})