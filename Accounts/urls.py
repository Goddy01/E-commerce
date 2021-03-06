from .views import vendor_reg_view, user_login_view, customer_reg_view, user_logout_view, must_auth
from django.urls import path

app_name = 'user'

urlpatterns = [
    path('v_reg/', vendor_reg_view, name='v_reg'),
    path('c_reg/', customer_reg_view, name='c_reg'),
    # path('v_login/', vendor_login_view, name='v_login'),
    path('login/', user_login_view, name="login"),
    path('logout/', user_logout_view, name='logout'),
    path('must_auth/', must_auth, name='must_auth')
]