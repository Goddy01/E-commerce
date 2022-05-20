from .views import vendor_reg_view, vendor_login_view
from django.urls import path

app_name = 'vendor'

urlpatterns = [
    path('reg/', vendor_reg_view, name='registration'),
    path('login/', vendor_login_view, name='login')
]