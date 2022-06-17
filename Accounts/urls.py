from .views import vendor_reg_view, vendor_login_view, customer_reg_view, customer_login_view, user_logout_view
from django.urls import path

app_name = 'user'

urlpatterns = [
    path('v_reg/', vendor_reg_view, name='v_reg'),
    path('c_reg/', customer_reg_view, name='c_reg'),
    path('v_login/', vendor_login_view, name='v_login'),
    path('c_login/', customer_login_view, name="c_login"),
    path('logout/', user_logout_view, name='logout'),
]