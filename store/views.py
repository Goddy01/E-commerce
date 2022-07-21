import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from .forms import AddProductForm,BillingForm
from Accounts.models import Vendor, User, Customer
from store.models import Product, Order, OrderItem
# Create your views here.

def store(request):
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(customer=request.user, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        order = {'get_cart_total':0, 'get_cart_items':0}
        items = []
        cart_items = order['get_cart_items']
    context = {'items':items, 'cart_items':cart_items}
    return render(request, 'base.html', context)

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


def cart(request):
    context = {}
    if request.user.is_authenticated:
        user = request.user
        order = Order.objects.filter(customer=user).order_by('-id').first()
        items = order.orderitem_set.all()
        print(len(items))
        if len(items) == 0:
            return HttpResponse('Your cart is empty.')
        else:
            order.total_order_price = order.get_cart_total + 10
            subtotal = order.get_cart_total
            order.save()
            for item in items:
                if item.quantity <= 0 :
                    item.delete()
            total = order.total_order_price

            context['sub_total'] = subtotal
            context['total'] = total
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        context['sub_total'] = 0
        context['total'] = 10

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

    order_item = OrderItem.objects.get(item_id=item_id)
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
        return HttpResponse('You must be authentiated to visit this page.')

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
        return HttpResponse('Your cart is empty. Nothing to checkout here.')
    else:
        subtotal = order.get_cart_total
        total = order.total_order_price
    

    context['sub_total'] = subtotal
    context['total'] = total
    context['billing_form'] = billing_form
    context['order'] = order
    context['items'] = items

    
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
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)