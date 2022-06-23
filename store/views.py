from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from .forms import AddProductForm
from Accounts.models import Vendor
from .models import Product
# Create your views here.
class HomeView(TemplateView):
    template_name = 'index.html'

class ShopView(TemplateView):
    template_name = 'shop.html'

class ShopDetailView(TemplateView):
    template_name = 'detail.html'

class CartView(TemplateView):
    template_name = 'cart.html'

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
        # print(add_form)
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
    m_products = Product.objects.filter(product_categories='M').order_by('?')
    f_products = Product.objects.filter(product_categories='W').order_by('?')
    mc_products = Product.objects.filter(product_categories='MC').order_by('?')
    fc_products = Product.objects.filter(product_categories='FC').order_by('?')
    context['m_products'] = m_products
    context['f_products'] = f_products
    context['mc_products'] = mc_products
    context['fc_products'] = fc_products
    return render(request, 'index.html', context)