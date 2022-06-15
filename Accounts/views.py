from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegForm, UserLoginForm
# Create your views here.
def user_reg_view(request):
    msg = None
    if request.method == 'POST':
        form = UserRegForm(request.POST)
        if form.is_valid():
            form.save()
            msg = 'Account created successfully'
            return redirect('vendor:login')
        else:
            msg = 'Form is Invalid!'
    else:
        form = UserRegForm()
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

            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)
                print(user.type)
                if user.type == "CUSTOMER":
                    return redirect('checkout')
                elif user.type == "VENDOR":
                    return redirect('add product')
                # return redirect('checkout')
            else:
                msg = 'User does not exist.'
        else:
            msg = 'Validation Error'
    return render(request, 'Accounts/login.html', {
        'form': form,
        'msg': msg,
    })

    return render()