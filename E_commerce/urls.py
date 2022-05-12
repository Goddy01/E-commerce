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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from store.views import (
    HomeView, ContactView,
    ShopDetailView, ShopView,
    CartView, CheckoutView,
    AddProductView,
    )
from seller_acct.views import vendor_reg_view, vendor_login_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('shop', ShopView.as_view(), name='shop'),
    path('shop_details', ShopDetailView.as_view(), name='shop detail'),
    path('cart', CartView.as_view(), name='cart'),
    path('checkout', CheckoutView.as_view(), name='checkout'),
    path('contact', ContactView.as_view(), name='contact'),
    path('add-product', AddProductView.as_view(), name='add product'),
    path('vendor-login', vendor_reg_view, name='vendor reg'),
    path('vendor-reg/', vendor_login_view, name='vendor login'),
]





if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)