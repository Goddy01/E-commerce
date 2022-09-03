from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from datetime import datetime
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from store.models import BillingAddress, Order, OrderItem
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
            print('BOOL RE: ', request.POST.get('bool'))
            if request.session.get('total') == order.total_order_price and request.POST.get('bool') == 'True':
                print('YEAHHHHHH')
                items = OrderItem.objects.filter(order=order)
                for item in items:
                    item.product.number_available -= item.quantity
                    item.product.save()
                order.complete = not order.complete
                # return 
            if request.POST.get('bool') != 'True':
                print('NAHHHHHH')
                order.complete = order.complete
            order.save()
            # messages.success(request, 'Your order has been placed. Thank you for patronizing us!')
    else:
        return redirect('user:must_auth')
    return render(request, 'make_payment.html', {'total': request.session.get('total'), 'email': request.session.get('email')})