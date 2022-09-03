from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from datetime import datetime
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from store.models import BillingAddress, Order
from Accounts.models import Vendor

def make_payment(request):
    vendors = Vendor.objects.all()
    for vendor in vendors:
        if vendor.username == request.user.username:
            return HttpResponse("You must create a Customer Account to be able to access customers' privileges.")
    if request.user.is_authenticated:
        order = Order.objects.filter(customer__email=request.user.email).order_by('-id').first()
        if order.total_order_price is None:
            return redirect('home')
        else:
            request.session['total'] = order.total_order_price
            request.session['email'] = request.user.email
            if request.session.get('total') == order.total_order_price:
                order.complete = not order.complete
            order.save()
    else:
        return redirect('user:must_auth')
    return render(request, 'make_payment.html', {'total': request.session.get('total'), 'email': request.session.get('email')})