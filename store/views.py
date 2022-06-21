from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from .forms import AddProductForm
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
    
    if request.method == "POST":
        add_form = AddProductForm(request.POST, request.FILES)
        print(add_form)
        if add_form.is_valid():
            obj = add_form.save(commit=False)
            seller = Vendor.objects.filter(email=request.user.email).first()
            obj.seller = seller
            obj.save()
            context['success'] = 'Product has been added.'
        # else:
        #     return HttpResponse('buggy')

    else:
        add_form = AddProductForm()
    context['add_product_form'] = add_form
    return render(request,'store/create_product.html',context)
