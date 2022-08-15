from Accounts.models import Customer
from .models import Order
# from django.contrib.auth.decorators import login_required

# @login_required
def website_content(request):
    # if not request.user.is_authenticated:
    # 
    # else:     
    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(username=request.user.username)
        except:
            customer = Customer.objects.get(device=request.session.get('device'))
    if request.user.id == None:
        customer = Customer.objects.get(device=request.session.get('device'))
    try:    
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    except:
        order = Order.objects.filter(customer=customer).order_by('-id').first()
    if order.complete == False:
        try:
            items = order.orderitem_set.all()
        except AttributeError:
            # pass
            items=0
            cart_items=0
        else:
            subtotal = order.get_cart_total
            cart_items = order.get_cart_items
            # print('cartitems: ', cart_items)
            for item in items:
                if item.product.number_available == 0:
                    cart_items -= item.quantity
                if item.quantity > item.product.number_available:
                    cart_items -= item.quantity
                    cart_items += item.product.number_available
    else:
        items=0
        cart_items=0
    context = {
        'items':items, 
        'cart_items': cart_items,
                    }
    return context