from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import VendorRegForm, VendorLoginForm
# Create your views here.
def vendor_reg_view(request):
    msg = None
    if request.method == 'POST':
        form = VendorRegForm(request.POST)
        if form.is_valid():
            form.save()
            msg = 'Account created successfully'
            return redirect('vendor:login')
        else:
            msg = 'Form is Invalid!'

    else:
        form = VendorRegForm()
    return render(request, 'Vendors_Acct/register.html', {
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

            if user is not None:
                login(request, user)
                return redirect('checkout')
            else:
                msg = 'User does not exist.'
        else:
            msg = 'Validation Error'
    return render(request, 'Vendors_Acct/login.html', {
        'form': form,
        'msg': msg,
    })

    return render()