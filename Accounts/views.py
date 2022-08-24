from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import (
    CustomerRegForm, UserLoginForm, 
    VendorRegForm)
from .models import User
from store.models import Order, OrderItem
from phonenumber_field.phonenumber import PhoneNumber
import phonenumbers
# Create your views here.
def customer_reg_view(request):
    msg = None
    request.user.type = "CUSTOMER"
    if request.method == 'POST':
        form = CustomerRegForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            # print('Tephone: ', form.cleaned_data['first_phone_num'])
            raw_user = User.objects.get(device=request.session.get('device'))
            raw_user_orders = Order.objects.filter(customer=raw_user)
            raw_user.fullname=obj.fullname
            raw_user.username=obj.username
            raw_user.address=obj.address
            x = phonenumbers.parse(f"{obj.first_phone_num}", None)
            raw_user.first_phone_num=phonenumbers.format_number(x, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            raw_user.email=obj.email
            raw_user.device=obj.device
            raw_user.set_password(request.POST['password1'])
            raw_user.save()
            print('Orders', raw_user_orders)
            for raw_user_order in raw_user_orders:
                raw_user_order.customer.fullname=obj.fullname
                raw_user_order.customer.username=obj.username
                raw_user_order.customer.address=obj.address
                x = phonenumbers.parse(f"{obj.first_phone_num}", None)
                raw_user_order.customer.first_phone_num=phonenumbers.format_number(x, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
                raw_user_order.customer.email=obj.email
                raw_user_order.customer.device=obj.device
                raw_user_order.save()
            form.device = request.session.get('device')
            # print('Form Device is: ', form.device)
            msg = 'Account created successfully'
            login(request, raw_user)
            request.session['device'] = []
            return redirect('checkout')
        else:
            msg = 'Form is Invalid!'
    else:
        form = CustomerRegForm()
    return render(request, 'Accounts/register.html', {
        'form': form, 
        'msg': msg, 
        })

def vendor_reg_view(request):
    msg = None
    request.user.type = "VENDOR"
    if request.method == 'POST':
        form = VendorRegForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.device = request.session.get('device')
            user = form.save()
            msg = 'Account created successfully'
            login(request, user)
            return redirect('add-product')
        else:
            msg = 'Form is Invalid!'
    else:
        form = VendorRegForm()
    return render(request, 'Accounts/register.html', {
        'form': form, 
        'msg': msg, 
        })

def user_login_view(request):
    form = UserLoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            # username=form.cleaned_data.get('username')

            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)
                # print(user.type)
                if user.type == "CUSTOMER":
                    try:    
                        cookie_order = Order.objects.get(customer__device=request.session.get('device'))
                    except:
                        pass
                    else:
                        try:
                            user_order, created = Order.objects.get_or_create(customer__email=email)
                        except:
                            user_order = Order.objects.filter(customer__email=email).order_by('-id').first()
                        # if len(user_order) > 0:
                        cookie_orderitems = cookie_order.orderitem_set.all()
                        user_orderitems = user_order.orderitem_set.all()
                        if len(user_orderitems) > 0:
                            for cookie_orderitem in cookie_orderitems:
                                for user_orderitem in user_orderitems:
                                    if cookie_orderitem.product.product_name == user_orderitem.product.product_name:
                                        user_orderitem.quantity += cookie_orderitem.quantity
                                        print('new_q: ', user_orderitem.quantity, 'cookie_own: ', cookie_orderitem.quantity)
                                        user_orderitem.save()
                                    if cookie_orderitem.product.product_name != user_orderitem.product.product_name:
                                        print('Hin no dey')
                                        # user_orderitem.append(cookie_orderitem)
                                        a = OrderItem.objects.create(
                                            order = user_order,
                                            product = cookie_orderitem.product,
                                            quantity = cookie_orderitem.quantity,
                                            size = cookie_orderitem.size,
                                            color = cookie_orderitem.color
                                        )
                                        print('color is: ', a.color)
                                        user_orderitem.save()
                            cookie_order.delete()
                        else:
                            if cookie_order:
                                print('notedey')
                                customer = User.objects.get(email=email)
                                cookie_order.customer = customer
                                cookie_order.save()
                        return redirect('home')
                    return redirect('home')
                elif user.type == "VENDOR":
                    return redirect('add-product')
                # return redirect('checkout')
            # if user.type != "CUSTOMER":
            #     return HttpResponse('Sorry you do not have a Customer account with us.')
            else:
                msg = 'User does not exist.'
        else:
            msg = 'Validation Error'
    return render(request, 'Accounts/login.html', {
        'form': form,
        'msg': msg,
    })

# def vendor_login_view(request):
#     form = VendorLoginForm(request.POST or None)
#     msg = None
#     if request.method == 'POST':
#         if form.is_valid():
#             email = form.cleaned_data.get('email')
#             password = form.cleaned_data.get('password')
#             user = authenticate(email=email, password=password)

#             if user is not None:
#                 login(request, user)
#                 return redirect('add product')
#             # if user.type != "VENDORR":
#             #     return HttpResponse('Sorry you do not have a Vendor account with us.')
#             else:[[[[[[[[[[
#                 msg = 'User does not exist.'
#         else:
#             msg = 'Validation Error'
#     return render(request, 'Accounts/login.html', {
#         'form': form,
#         'msg': msg,
#     })

@login_required
def user_logout_view(request):
    logout(request)
    return redirect('home')
def must_auth(request):
    return render(request, 'Accounts/must_auth.html')