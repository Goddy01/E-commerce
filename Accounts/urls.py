from .views import vendor_reg_view, user_login_view, customer_reg_view, user_logout_view
from django.urls import path

app_name = 'user'

urlpatterns = [
    path('v_reg/', vendor_reg_view, name='v_reg'),
    path('c_reg/', customer_reg_view, name='c_reg'),
    path('login/', user_login_view, name='login'),
    path('logout/', user_logout_view, name='logout'),
]