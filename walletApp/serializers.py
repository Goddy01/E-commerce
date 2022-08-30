from .models import Wallet, WalletTransaction
from rest_framework import serializers
from django.db.models import Sum
# from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.conf import settings
import requests

class WalletSerializer(serializers.ModelSerializer):
    """
    Serializers to validate the user's wallet 
    """
    balance = serializers.SerializerMethodField()

    def get_balance(self, obj):
        bal = WalletTransaction.objects.filter(
            wallet=obj, status="success").aggregate(Sum('amount'))['amount__sum']
        return bal

    class Meta:
        model = Wallet
        fields = ['id', 'currency', 'balance']