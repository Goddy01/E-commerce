from .views import user_reg_view, user_login_view
from django.urls import path

app_name = 'user'

urlpatterns = [
    path('reg/', user_reg_view, name='registration'),
    path('login/', user_login_view, name='login')
]