from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import (
    CustomerRegForm, CustomerLoginForm, 
    VendorRegForm, VendorLoginForm)

# Create your views here.
def customer_reg_view(request):
    msg = None
    request.user.type = "CUSTOMER"
    if request.method == 'POST':
        form = CustomerRegForm(request.POST)
        if form.is_valid():
            form.save()
            msg = 'Account created successfully'
            return redirect('user:c_login')
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
            form.save()
            msg = 'Account created successfully'
            return redirect('user:v_login')
        else:
            msg = 'Form is Invalid!'
    else:
        form = VendorRegForm()
    return render(request, 'Accounts/register.html', {
        'form': form, 
        'msg': msg, 
        })

def customer_login_view(request):
    form = CustomerLoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = authenticate(email=email, password=password)

            if user is not None and request.user.type == "CUSTOMER":
                login(request, user)
                # print(user.type)
                return redirect('checkout')
                # return redirect('checkout')
            if request.user.type != "CUSTOMER":
                return HttpResponse('Sorry you do not have a Customer account with us.')
            else:
                msg = 'User does not exist.'
        else:
            msg = 'Validation Error'
    return render(request, 'Accounts/login.html', {
        'form': form,
        'msg': msg,
    })

def vendor_login_view(request):
    form = VendorLoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = authenticate(email=email, password=password)

            if user is not None and request.user.type == "VENDOR":
                login(request, user)
                return redirect('add product')
            if request.user.type != "VENDORR":
                return HttpResponse('Sorry you do not have a Vendor account with us.')
            else:
                msg = 'User does not exist.'
        else:
            msg = 'Validation Error'
    return render(request, 'Accounts/login.html', {
        'form': form,
        'msg': msg,
    })

@login_required
def user_logout_view(request):
    logout(request)
    return redirect('home')