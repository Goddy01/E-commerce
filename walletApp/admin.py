from django.contrib import admin
from .models import Payment, WalletTransaction
# Register your models here.

admin.site.register(Payment)
admin.site.register(WalletTransaction)