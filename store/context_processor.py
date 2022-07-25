import json
from store.models import Product
from django.shortcuts import render
from .models import Order

def website_content(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=request.user, complete=False)
        items = order.orderitem_set.all()
        subtotal = order.get_cart_total
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

            product = Product.objects.get(product_id=item)
            order['get_cart_total'] += (product.product_price * cart[item]['quantity'])
            order['get_cart_items'] += cart[item]['quantity']

            item = {
                'product':{
                        'product': product},
                'quantity': cart[item]['quantity'],
                'get_items_price': cart[item]['quantity'] * product.product_price,
            }
            items.append(item)
    context = {'items':items, 'cart_items':cart_items}
    return context