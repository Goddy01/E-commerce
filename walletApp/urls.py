from django.urls import path
from .views import make_payment
app_name = 'wallet'

urlpatterns = [
    path('make-payment/', make_payment, name='make-payment'),
]