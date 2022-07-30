import json
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from .forms import AddProductForm,BillingForm
from Accounts.models import Vendor, User, Customer
from store.models import Product, Order, OrderItem
# Create your views here.

# def store(request):
#     if request.user.is_authenticated:
#         order, created = Order.objects.get_or_create(customer=request.user, complete=False)
#         items = order.orderitem_set.all()
#         cart_items = order.get_cart_items
#     else:
#         try:
#             cart = json.loads(request.COOKIES['cart'])
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

class ShopDetailView(TemplateView):
    template_name = 'detail.html'

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
    products = Product.objects.all().order_by('?').distinct()[:6]
    latest_products = Product.objects.all().order_by('-product_id')[:9]
    # f_products = Product.objects.all().filter(product_categories='W').order_by('?')[:1]
    # mc_products = Product.objects.all().filter(product_categories='MC').order_by('?')[:1]
    # fc_products = Product.objects.all().filter(product_categories='FC').order_by('?')[:1]
    context['products'] = products
    context['latest_products'] = latest_products
    # context['f_products'] = f_products
    # context['mc_products'] = mc_products
    # context['fc_products'] = fc_products
    return render(request, 'store/index.html', context)


def add_to_cart(request, product_id):
    product = Product.objects.get(product_id=product_id)

    try:
        customer = request.user
    except:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    # orderitems = order.orderitem_set.all()
    item, created = OrderItem.objects.create(product=product, order=order)
    if item.quantity <= 0 or item.product.number_available == 0:
        order.get_cart_total -= item.get_items_price
        order.save()
        item.delete()
        if item.quantity > item.product.number_available:
            item.quantity = item.product.number_available
    return render(request, 'store/index.html')

def cart(request):
    context = {}
    # if request.user.is_authenticated:
    try:
        user = request.user
    except:
        device = request.COOKIES['device']
        print('Device is: ', device)
        user = Customer.objects.get_or_create(device=device)
    # print(Order.objects.filter(customer=user).order_by('-id').first().complete)
    try:
        if Order.objects.filter(customer=user).order_by('-id').first().get_cart_total == 0:
            return redirect('no_cart')
    except TypeError:
        return redirect('no_cart')
    order = Order.objects.filter(customer=user).order_by('-id').first()
    items = order.orderitem_set.all()
    for item in items:
        if item.quantity <= 0 or item.product.number_available == 0:
            order.get_cart_total -= item.get_items_price
            order.save()
            item.delete()
        if item.quantity > item.product.number_available:
            item.quantity = item.product.number_available
    # print(item)
    # print(len(items))
    if len(items) == 0:
        order.save(commit=False)
        order.total_order_price = 10
        order.save()
        # print('Get Total1: ', order.total_order_price)
        return redirect('no_cart')
    else:
        print('Get Total2: ', order.total_order_price)
        order.total_order_price = order.get_cart_total + 10
        subtotal = order.get_cart_total
        order.save()
        total = order.total_order_price

    # else:
    #     try:
    #         cart = json.loads(request.COOKIES['device'])
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
                    obj = billing_form.save(commit=False)
                    obj.customer = Customer.objects.get(username=request.user.username)
                    obj.order = Order.objects.filter(customer=user).order_by('-id').first()
                    obj.order.complete = True
                    obj.order.save()
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

            order = Order.objects.filter(customer=user).order_by('-id').first()
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

@csrf_exempt
def updateItem(request):
    data = json.loads(request.body)
    print(data)
    productId = data['productId']
    action = data['action']

    print('ProuctId:', productId)
    print('Action:', action)

    customer = request.user
    product = Product.objects.get(product_id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        if orderItem.quantity < product.number_available:
            orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    elif action == 'del':
        orderItem.delete()
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)


def no_cart(request):
    return render(request, 'store/no_cart.html')

def no_checkout(request):
    return render(request, 'store/no_checkout.html')
