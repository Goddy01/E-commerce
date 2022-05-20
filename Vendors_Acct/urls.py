from .views import vendors_reg__view, vendors_login_view
from django.urls import path
app_name = 'Vendors_Acct'

url_patterns = [
    path('vendors-reg/', vendors_reg__view, name='vendors_reg'),
    path('vendors-login', vendors_login_view, name='vendors_login')
]