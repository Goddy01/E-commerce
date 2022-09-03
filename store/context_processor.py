import uuid
from Accounts.models import Customer, User, Vendor
from .models import Order
# from django.contrib.auth.decorators import login_required

# @login_required
def website_content(request):
    # if not request.user.is_authenticated:
    # 
    # else:
    customers = Customer.objects.all()
    vendors = Vendor.objects.all()
    try:
        user = User.objects.get(device=request.session['device'])
    except:
        # if request.session.get('device') == []:
        device = str(uuid.uuid4())
        request.session['device'] = device
        user = User.objects.create(
            fullname=request.session['device'],
            username=request.session['device'],
            email=request.session['device'] + '@gmail.com',
            address=request.session['device'],
            first_phone_num='1',
            device=request.session['device'],

            )
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
                    # cart_items += 0
    else:
        items=0
        cart_items=0
    if request.user.is_authenticated and Order.objects.filter(customer__email=request.user.email).order_by('-id').first().get_cart_total != 0:
        order = Order.objects.filter(customer__email=request.user.email).order_by('-id').first()
        total = order.total_order_price
        email = request.user.email
    context = {
        'items':items, 
        'cart_items': cart_items,
        'customers': customers,
        'vendors': vendors,}
    return context