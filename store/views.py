import json, uuid
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView
from .forms import AddProductForm, OrderItemForm, BillingForm
from Accounts.models import Vendor, User, Customer
from store.models import Product, Order, OrderItem
# Create your views here.

import phonenumbers
from faker.providers.phone_number.en_US import Provider

class CustomPhoneProvider(Provider):
    def phone_number(self):
        while True:
            phone_number = self.numerify(self.random_element(self.formats))
            parsed_number = phonenumbers.parse(phone_number, 'US')
            if phonenumbers.is_valid_number(parsed_number):
                return phonenumbers.format_number(
                    parsed_number,
                    phonenumbers.PhoneNumberFormat.E164
                )
# def store(request):
#     if request.user.is_authenticated:
#         order, created = Order.objects.get_or_create(customer=request.user, complete=False)
#         items = order.orderitem_set.all()
#         cart_items = order.get_cart_items
#     else:
#         try:
#             cart = json.loads(request.session['cart'])
#         except KeyError:
#             cart = {}
#         order = {'get_cart_total':0, 'get_cart_items':0}
#         items = []
#         cart_items = order['get_cart_items']
#         for item in cart:
#             cart_items += cart[item]['quantity']
#     context = {'items':items, 'cart_items':cart_items}
    # return render(request, 'base.html', context)

class ShopView(TemplateView):
    template_name = 'shop.html'

# class ShopDetailView(TemplateView):
#     template_name = 'detail.html'

class ContactView(TemplateView):
    template_name = 'contact.html'

def add_product_view(request):
    """The view for vendors to add products to the store"""
    user = request.user

    if not user.is_authenticated:
        return redirect('user:login')

    context = {}
    
    if request.method == "POST":
        add_form = AddProductForm(request.POST, request.FILES)
        
        if add_form.is_valid():
            obj = add_form.save(commit=False)
            # seller = Vendor.objects.filter(email=request.user.email).first()
            obj.seller = request.user
            obj.save()
            context['success'] = 'Product has been added.'
        # else:
        #     return HttpResponse('buggy')
            

    else:
        add_form = AddProductForm()
    context['add_product_form'] = add_form
    return render(request,'store/create_product.html',context)

def home_page(request):
    context = {}
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
    products = Product.objects.all().order_by('?').distinct()[:6]
    latest_products = Product.objects.all().order_by('-product_id')[:9]
    context['products'] = products
    context['latest_products'] = latest_products
    return render(request, 'store/index.html', context)

def add_to_cart(request, product_id):
    # print(request.method)
    # try:
    #     customer = Customer.objects.get(device=request.session['device'])
    # except:
    #     request.session['device'] = str(uuid.uuid4())
    #     customer = Customer.objects.create(device=request.session['device'])
    if not request.user.is_authenticated:
        user = User.objects.get(device=request.session.get('device'))
        customer = Customer.objects.get(device=user.device)
    else:
        customer = Customer.objects.get(username=request.user.username)
    product = Product.objects.get(product_id=product_id)
    print('DEVICE IS: ', request.session['device'])
    try:    
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    except:
        order = Order.objects.filter(customer=customer).order_by('-id').first()
    # orderitems = []
    orderitem, created = OrderItem.objects.get_or_create(product=product, order=order)
    COLOR_CHOICES = []
    SIZE_CHOICES = []
    for color in product.product_colors.split(','):
        color = color.strip()
        COLOR_CHOICES.append((color, color))
        # order_item.save()
    for size in product.product_sizes.split(','):
        size = size.strip()
        SIZE_CHOICES.append((size, size))
    if request.method == 'POST':
        print('amazon')
        orderitemform = OrderItemForm(data=request.POST, size_choices=SIZE_CHOICES, color_choices=COLOR_CHOICES)
        # print('errors re: ', orderitemform.errors)
        for field in orderitemform:
            for error in field.errors:
                print('ERROR: ', error)
        print('color: ', request.POST.get('color'))
        print('size: ', request.POST.get('size'))
        print('qty is: ', request.POST.get('quantity'))
        print('form: ', orderitemform)
        print(orderitemform.is_valid())
        print(orderitemform.is_bound)
        if orderitemform.is_valid():
            print('yaga')
            obj = orderitemform.save(commit=False)
            orderitem.quantity = obj.quantity
            orderitem.size = obj.size
            orderitem.color = obj.color
            print('color is na: ', orderitem.color)
            orderitem.save()
    # orderitem.ordered_product_color = 
    # print('opc is: ', orderitem.ordered_product_color)
    # print('ops is: ', orderitem.ordered_product_size)
    # print('ops type is: ', tuple(orderitem.ordered_product_size))
    # print('qty is: ', orderitem.quantity)
    if orderitem.quantity <= 0:
        orderitem.quantity = 0
    elif orderitem.quantity > product.number_available:
        orderitem.quantity = product.number_available
    # elif orderitem.quantity < product.number_available:
    #     orderitem.quantity += 1
    orderitem.save()
    # orderitems.append(orderitem)
    context = {
        'product': product,
    }
    if True:
        return redirect('home')
    return render(request, 'store/detail.html', context)

def cart(request):
    context = {}
    # if request.user.is_authenticated:
    # print('Mr User',request.session['device'])
    if request.user.is_authenticated:
        user = request.user
    else:
        user = Customer.objects.get(device=request.session.get('device'))
    # try:
    print('first', Order.objects.filter(customer=user).order_by('-date_ordered').first())
    # print('1', Order.objects.filter(customer=user).order_by('-id')[1])
    print('latest', Order.objects.filter(customer=user).order_by('-id').first())
    print('latest2', Order.objects.filter(customer=user).order_by('-id').first())
    if Order.objects.filter(customer=user).order_by('-id').first() is not None:
        if Order.objects.filter(customer=user).order_by('-id').first().get_cart_total == 0:
            print('brozo')
            return redirect('no_cart')
    else:
        return redirect('home')
    # order, created = Order.objects.get_or_create(customer=user, complete=False)
    try:    
        order, created = Order.objects.get_or_create(customer=user, complete=False)
        print('order1:', order)
    except:
        order = Order.objects.filter(customer=user).order_by('-id').first()
        print('order2:', order)
    # if order.complete == False:
    items = order.orderitem_set.all()
    for item in items:
        if item.quantity <= 0 or item.product.number_available == 0:
            order.get_cart_total -= item.get_items_price
            order.save()
            item.delete()
        if item.quantity > item.product.number_available:
            item.quantity = item.product.number_available
            item.save()
    # print(item)
    # print(len(items))
    if len(items) == 0:
        # try:
        #     order.save(commit=False)
        # except TypeError:
        #     order[1].save(commit=False)
        order.total_order_price = 10
        order.save()
        # print('Get Total1: ', order.total_order_price)
        print('brozo1.0')
        return redirect('no_cart')
    else:
        print('Get Total2: ', order.total_order_price)
        order.total_order_price = order.get_cart_total + 10
        subtotal = order.get_cart_total
        order.save()
        total = order.total_order_price

    # else:
    #     try:
    #         cart = json.loads(request.session['device'])
    #     except KeyError:
    #         cart = {}
    #     print(cart)

    #     # print(items)
    #     for item in items:
    #             if item['product']['number_available'] == 0:
    #                 items.remove(item)
    #             if item['product']['number_available'] < item['quantity']:
                    # item['quantity'] = item['product']['number_available']
    # try:
    context['sub_total'] = subtotal
    context['total'] = total
    context['order'] = order
    context['items'] = items
    # except UnboundLocalError:
        # return redirect('no_cart')
    return render(request, 'store/cart.html', context)


def quantity_increment(request, item_id):
    order_item = OrderItem.objects.get(item_id=item_id)
    if order_item.quantity < order_item.product.number_available:
        order_item.quantity += 1
        
    else:
        order_item.quantity = order_item.product.number_available
    order_item.save()
    subtotal = order_item.order.get_cart_total
    total = subtotal + 10
    i = 1
    if i == 1:
        return redirect('cart')
    return render(request, 'store/cart.html', {'sub_total':subtotal, 'total':total})
    

def quantity_decrement(request, item_id):

    try:
        order_item = OrderItem.objects.get(item_id=item_id)
    except ObjectDoesNotExist:
        # order_item.delete()
        return redirect('cart')
    else:
        if order_item.quantity <=  0:
            order_item.delete()
        else:
            order_item.quantity -= 1
            order_item.save()
        i = 1
        if i == 1:
            return redirect('cart')
        subtotal = order_item.order.get_cart_total
        total = subtotal + 10
    return render(request, 'store/cart.html', {'sub_total':subtotal, 'total':total})


def delete_order_item(request, item_id):
    order_item = OrderItem.objects.get(item_id=item_id)
    o = order_item
    subtotal = order_item.order.get_cart_total - order_item.get_items_price
    total = subtotal + 10
    order_item.delete()
    i = 1
    if i == 1:
        return redirect('cart')

    return render(request, 'store/cart.html', {'sub_total':subtotal, 'total':total})



def checkout(request):
    context = {}
    user = request.user

    if not user.is_authenticated:
        return redirect('user:must_auth')

    order = Order.objects.filter(customer=user).order_by('-id').first()
    if order is not None:
        if Order.objects.filter(customer=user).order_by('-id').first().get_cart_total == 0:
            return redirect('no_checkout')
        else:
            if request.method == 'POST':
                billing_form = BillingForm(request.POST)
                if billing_form.is_valid():
                    print('yooo')
                    obj = billing_form.save(commit=False)
                    obj.customer = Customer.objects.get(username=request.user.username)
                    obj.order = Order.objects.filter(customer=user).order_by('-id').first()
                    obj.order.complete = True
                    obj.order.save()
                    order.complete = True
                    order.save()
                    obj.save()

                    items = OrderItem.objects.filter(order=obj.order)
                    for item in items:
                        item.product.number_available -= item.quantity
                        item.product.save()
                    billing_form= obj

                    i = 0
                    if i == 0:
                        return redirect('home')
            else:
                billing_form = BillingForm()

            try:    
                order, created = Order.objects.get_or_create(customer=user, complete=False)
            except:
                order = Order.objects.filter(customer=user).order_by('-id').first()
            # order = Order.objects.filter(customer=user).order_by('-id').first()
            items = order.orderitem_set.all()
            
            
            if len(items) == 0:
                return redirect('no_checkout')
            else:
                subtotal = order.get_cart_total
                total = order.total_order_price
        

            context['sub_total'] = subtotal
            context['total'] = total
            context['billing_form'] = billing_form
            context['order'] = order
            context['items'] = items

    else:
        return redirect('no_checkout')

    
    return render(request, 'store/checkout.html', context)


# def load_cities(request):
#     country_id = request.GET.get('country')
#     cities = City.objects.filter(country_id=country_id).order_by('name')
#     return render(request, 'store/checkout.html', {'cities': cities})

# @csrf_exempt
# def updateItem(request):
#     data = json.loads(request.body)
#     print(data)
#     productId = data['productId']
#     action = data['action']

#     print('ProuctId:', productId)
#     print('Action:', action)

#     customer = request.user
#     product = Product.objects.get(product_id=productId)
#     order, created = Order.objects.get_or_create(customer=customer, complete=False)
#     orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

#     if action == 'add':
#         if orderItem.quantity < product.number_available:
#             orderItem.quantity += 1
#     elif action == 'remove':
#         orderItem.quantity -= 1
#     elif action == 'del':
#         orderItem.delete()
#     orderItem.save()

#     if orderItem.quantity <= 0:
#         orderItem.delete()
#     return JsonResponse('Item was added', safe=False)


def no_cart(request):
    return render(request, 'store/no_cart.html')

def no_checkout(request):
    return render(request, 'store/no_checkout.html')


def product_details(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    try:
        order_item, created = OrderItem.objects.get_or_create(product=product, order__customer__email=request.user.email)
    except:
        order_item, created = OrderItem.objects.get_or_create(product=product, order__customer__device=request.session.get('device'))
    # print('Na the orderitem be this: ', order_item)
    # print('def re: ', order_item.ordered_product_color)
    COLOR_CHOICES = []
    SIZE_CHOICES = []
    for color in order_item.ordered_product_color:
        color = color.strip()
        COLOR_CHOICES.append((color, color))
        # order_item.save()
    for size in order_item.ordered_product_size:
        size = size.strip()
        SIZE_CHOICES.append((size, size))

    orderitemform = OrderItemForm(SIZE_CHOICES, COLOR_CHOICES)
    product_sizes = product.product_sizes.split(',')
    product_colors = product.product_colors.split(',')
    context = {
        'product': product,
        'product_sizes': product_sizes,
        'product_colors': product_colors,
        'orderitemform': orderitemform,
    }
    # product_sizes = 
    return render(request, 'store/detail.html', context)