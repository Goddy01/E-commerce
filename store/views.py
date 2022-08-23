import json, uuid
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView
from .forms import AddProductForm, OrderItemForm, BillingForm
from Accounts.models import Vendor, User, Customer
from store.models import Product, Order, OrderItem
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
    # return render(request, 'store/index.html', context)

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

        if orderitemform.is_valid():
            print('yaga')
            # obj = orderitemform.save(commit=False)
            orderitem.size = orderitemform.cleaned_data['size']
            orderitem.color = orderitemform.cleaned_data['color']
            sum_qty = orderitemform.cleaned_data['quantity'] + orderitem.quantity
            # print(sum_qty)
            if orderitemform.cleaned_data['quantity'] > orderitem.product.number_available:
                orderitem.quantity += 0
                messages.error(request, 'Quantity more than available product.')
                OrderItemForm(size_choices=SIZE_CHOICES, color_choices=COLOR_CHOICES)
            elif orderitemform.cleaned_data['quantity'] < orderitem.product.number_available and orderitemform.cleaned_data['quantity'] != 0:
                if sum_qty <= orderitem.product.number_available:
                    orderitem.quantity += orderitemform.cleaned_data['quantity']
                    messages.success(request, 'Item has been added to Cart.')
                else:
                    messages.error(request, 'Quantity added more than the available product number.')
            elif orderitemform.cleaned_data['quantity'] <= 0:
                orderitem.quantity += 0
                messages.error(request, 'You must add at least one item.')
            orderitem.save()
    else:
        orderitemform = OrderItemForm(size_choices=SIZE_CHOICES, color_choices=COLOR_CHOICES)

    if orderitem.quantity <= 0:
        orderitem.quantity = 0
    orderitem.save()
    context = {
        'product': product,
        'orderitemform': orderitemform,
    }
    # if True:
    #     return redirect('home')
    return render(request, 'store/detail.html', context)

def cart(request):
    context = {}

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

    if len(items) == 0:
        
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

    context['sub_total'] = subtotal
    context['total'] = total
    context['order'] = order
    context['items'] = items

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

                    messages.success(request, 'Your order has been made. Thank you for patronizing us!')
                    # i = 0
                    # if i == 0:
                    #     return redirect('home')
                else:
                    messages.error(request, 'Unable to checkout.')
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

def get_product_queryset(request):
    """The view that performs the search functionality"""
    if request.method == 'GET':
        query = request.GET.get('query')

        if query is not None:
            products = Product.objects.filter(
                Q(product_name__icontains=query) | Q(product_description__icontains=query)
            ).distinct()

            if not products:
                return HttpResponse('No search result for this query.')
            context = {
                'results': products,
            }

            return render(request, 'store/index.html', context)
        else:
            return render(request, 'store/index.html')
    else:
        return render(request, 'store/index.html')

def pagination(request):
    products_list = Product.objects.all()
    page_number =   request.GET.get('page', 1)
    products_paginator = Paginator(products_list, 1)
    try:
        products = products_paginator.page(page_number)
    except PageNotAnInteger:
        products = products_paginator.page(1)
    except EmptyPage:
        products = products_paginator.page(products_paginator.num_pages)
    return render(request, 'store/index.html', {'products': products})