import json
from django.shortcuts import render
from .models import Order

def website_content(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=request.user, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except KeyError:
            cart = {}
        order = {'get_cart_total':0, 'get_cart_items':0}
        items = []
        cart_items = order['get_cart_items']
        for item in cart:
            cart_items += cart[item]['quantity']
    context = {'items':items, 'cart_items':cart_items}
    return context