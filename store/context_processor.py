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
        for item in items:
            if item.product.number_available == 0:
                cart_items -= item.quantity
            if item.quantity > item.product.number_available:
                cart_items -= item.quantity
                cart_items += item.product.number_available
        print('CartItems is ', cart_items)
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
                    'product_id': product.product_id,
                    'product_name': product.product_name,
                    'product_image1': product.product_image1,
                    'product_price': product.product_price,
                    'number_available': product.number_available,
                },
                'quantity': cart[item]['quantity'],
                'get_items_price': cart[item]['quantity'] * product.product_price,
            }
            items.append(item)
        for item in items:
            if item['product']['number_available'] == 0:
                items.remove(item)
                cart_items -= item['quantity']
            if item['product']['number_available'] < item['quantity']:
                cart_items -= item['quantity']
                cart_items += item['product']['number_available']
    context = {'items':items, 'cart_items':cart_items}
    return context