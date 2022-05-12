from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import VendorRegForm, VendorLoginForm

# Create your views here.
def vendor_reg_view(request):
    context = {}
    if request.method == 'POST':
        form = VendorRegForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            context['success_message'] = 'Account Creation Successful!'
            return redirect(login)
        else:
            context['form'] = form
    else:
        context['form'] = VendorRegForm()
    return render(request, 'seller_acct/register.html', context)



def vendor_login_view(request):
    context = {}
    if request.method == 'POST':
        form = VendorLoginForm(request.POST)

        if form.is_valid():
            email = request.POST.get('email').lower()
            password = request.POST.get('password')

            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('dashboard')
    else:
        form = VendorLoginForm()
    context['form'] = form
    return render(request, 'seller_acct/login.html', context)


