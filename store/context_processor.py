import uuid
from Accounts.models import Customer, User, Vendor
from .models import Order, WishList, Product
# from django.contrib.auth.decorators import login_required

# @login_required
def website_content(request):
    context = {}
    men = Product.objects.filter(product_categories=["M"]).count()
    women = Product.objects.filter(product_categories=["W"]).count()
    m_c = Product.objects.filter(product_categories=["MC"]).count()
    f_c = Product.objects.filter(product_categories=["FC"]).count()
    request.session[f'{request.user.username}_wish_counter'] = 0
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
        wish_count = WishList.objects.filter(customer=request.user).count()
        context['wish_count'] = wish_count
        request.session['wish_count'] = wish_count
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
    if Order.objects.filter(customer__email=request.user.email, customer__type='CUSTOMER'):
        if request.user.is_authenticated and Order.objects.filter(customer__email=request.user.email).order_by('-id').first().get_cart_total != 0:
            order = Order.objects.filter(customer__email=request.user.email).order_by('-id').first()
            total = order.total_order_price
            email = request.user.email

    context['items'] = items
    context['cart_items'] = cart_items
    context['customers'] = customers
    context['vendors'] = vendors
    context['men'] = men,
    context['women'] = women
    context['m_c'] = m_c
    context['f_c'] = f_c
    return context