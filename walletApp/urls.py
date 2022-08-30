from django.urls import path
from .views import initiate_payment
app_name = 'wallet'

urlpatterns = [
    path('initiate_payment/', initiate_payment, name="initiate_payment"),
    # path('deposit/', DepositFunds.as_view(), name="deposit"),
    # path('deposit/verify/<str:reference>/', VerifyDeposit.as_view(), name="verify_deposit"),
]