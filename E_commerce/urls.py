"""E_commerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from re import template
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from store.views import (
    HomeView, ContactView,
    ShopDetailView, ShopView,
    CartView, CheckoutView,
    AddProductView,
    )
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('shop', ShopView.as_view(), name='shop'),
    path('shop_details', ShopDetailView.as_view(), name='shop detail'),
    path('cart', CartView.as_view(), name='cart'),
    path('checkout', CheckoutView.as_view(), name='checkout'),
    path('contact', ContactView.as_view(), name='contact'),
    path('add-product', AddProductView.as_view(), name='add product'),
    path('vendors/', include('Vendors_Acct.urls', namespace='vendor')),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password/password_reset.html'), name='password reset'),
    
    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="password/password_reset_done.html"), name="pasword reset done"),
    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password/password_reset_form.html'), name="password reset confirm"),
    # path(),
    # path(),
    # path(),
]





if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)