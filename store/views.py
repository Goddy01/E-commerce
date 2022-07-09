from typing import OrderedDict
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from .forms import AddProductForm
from Accounts.models import Vendor
from store.models import Product, Order, OrderItem
# Create your views here.
# class HomeView(TemplateView):
#     template_name = 'store/index.html'

class ShopView(TemplateView):
    template_name = 'shop.html'

class ShopDetailView(TemplateView):
    template_name = 'detail.html'

class CheckoutView(TemplateView):
    template_name = 'checkout.html'

class ContactView(TemplateView):
    template_name = 'contact.html'

# class AddProductView(TemplateView):
#     template_name = 'create_product.html'

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
        order = Order.objects.filter(customer=user)
        # print(order.count())
        # print(order)
        if not order.exists():
            order, created = Order.objects.create(customer=user, complete=False), False
            # print(order.get_cart_total)
        else:
            order = Order.objects.filter(customer=user)
        items = OrderItem.objects.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
    order_total = 0
    for ord in order:
        order_total += ord.get_cart_total
    context['order_total'] = order_total
    context['order'] = order
    context['items'] = items
    return render(request, 'store/cart.html', context)


def quantity_increment(request, item_id):
    # context = {}
    # order_item = Order.objects.all()
    # customer = OrderItem.objects.get(order.customer=request.user)
    order_item = OrderItem.objects.get(item_id=item_id)
    order_item.quantity += 1
    order_item.save()

    # print(order_item)
    # value1 = value.orderitem_set.all()
    # orderitem.quantity += 1
    # orderitem.product.product_price += orderitem.product.product_price
    # orderitem.save()
    # context['order_item'] = order_item
    return render(request, 'store/cart.html')
    

def quantity_decrement(request, item_id):

    order_item = OrderItem.objects.get(item_id=item_id)
    order_item.quantity -= 1
    order_item.save()

    return render(request, 'store/cart.html')


def delete_order_item(request, item_id):
    order_item = OrderItem.objects.get(item_id=item_id)
    order_item.delete()
    # order_item.save()

    return render(request, 'store/cart.html')

