from django.utils import timezone as tz
from django.db import models
from Accounts.models import User
import secrets


# Create your models here.

class Payment(models.Model):
    amount =        models.DecimalField(max_digits=100, null=True, decimal_places=2)
    ref =           models.CharField(max_length=200)
    email =         models.EmailField()
    verified =      models.BooleanField(default=False)
    date_created =  models.DateTimeField(default=tz.now, null=True)

    class Meta:
        ordering = ('-date_created', )

    def __str__(self):
        return f"Payment: {self.amount}"

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)

    def amount_value(self) -> int:
        return self.amount
# class Wallet(models.Model):
#     user = models.OneToOneField(
#         User, null=True, on_delete=models.CASCADE)
#     currency = models.CharField(max_length=50, default='NGN')
#     created_at = models.DateTimeField(default=timezone.now, null=True)

#     def __str__(self):
#         return self.user.__str__()

# class WalletTransaction(models.Model):

#     TRANSACTION_TYPES = (
#         ('deposit', 'deposit'),
#         ('transfer', 'transfer'),
#         ('withdraw', 'withdraw'),
#     )
#     wallet = models.ForeignKey(Wallet, null=True, on_delete=models.CASCADE)
#     transaction_type = models.CharField(
#         max_length=200, null=True,  choices=TRANSACTION_TYPES)
#     amount = models.DecimalField(max_digits=100, null=True, decimal_places=2)
#     timestamp = models.DateTimeField(default=timezone.now, null=True)
#     status = models.CharField(max_length=100, default="pending")
#     paystack_payment_reference = models.CharField(max_length=100, default='', blank=True)

#     def __str__(self):
#         return self.wallet.user.__str__()