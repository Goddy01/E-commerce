from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import AddProduct
from Accounts.models import Vendor
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
    add_form = AddProduct(request.POST or None, request.FILES or None)
    if add_form.is_valid():
        add_form.save()
        # vendor = Vendor.objects.filter(email=user.email)
        # print(vendor)
        context['success_message'] = "Product has been posted."
        return redirect('home')
    else:
        add_form = AddProduct()
    context['add_product_form'] = add_form
    return render(request,'store/create_product.html',context)
