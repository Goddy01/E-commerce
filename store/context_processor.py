import json, uuid
from django.shortcuts import render, get_object_or_404
from .models import Order

def website_content(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=request.user, complete=False)
    else:
        request.session['nonuser'] = uuid.uuid4
        order = Order.objects.create(session_id=request.session['nonuser'], complete=False)
        # order = {'get_cart_total':0, 'get_cart_items':0}
        # items = []
        # cart_items = order.get_cart_items
    items = order.orderitem_set.all()
    cart_items = order.get_cart_items
    context = {'items':items, 'cart_items':cart_items}
    context = {'items':items, 'cart_items':cart_items}
    return context