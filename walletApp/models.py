from django.db import models
from Accounts.models import User
from django.utils import timezone

# Create your models here.


class Wallet(models.Model):
    user = models.OneToOneField(
        User, null=True, on_delete=models.CASCADE)
    currency = models.CharField(max_length=50, default='NGN')
    created_at = models.DateTimeField(default=timezone.now, null=True)

     def __str__(self):
        return self.user.fullname