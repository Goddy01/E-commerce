from django.urls import path
from .views import initiate_payment, verify_payment
app_name = 'wallet'

urlpatterns = [
    path('initiate_payment/', initiate_payment, name="initiate-payment"),
    # path('deposit/', DepositFunds.as_view(), name="deposit"),
    path('<str:ref>/', verify_payment, name="verify-payment"),
]