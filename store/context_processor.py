from Accounts.models import Customer
from .models import Order
from django.shortcuts import request
def website_conent(request):
    if not request.user.is_authenticated:
        customer = Customer.objects.get(device=request.session.get('device'))
    else:
        customer = Customer.objects.get(email=request.user.email)
    order = Order.objects.filter(customer=customer).order_by('-id').first()
    items = order.orderitem_set.all()
    subtotal = order.get_cart_total
    cart_items = order.get_cart_items
    for item in items:
        if item.product.number_available == 0:
            cart_items -= item.quantity
        if item.quantity > item.product.number_available:
            cart_items -= item.quantity
            cart_items += item.product.number_available
    context = {
        'items':items, 
        'cart_items': cart_items,
                    }
    return context