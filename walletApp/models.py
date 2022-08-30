from django.utils import timezone as tz
from django.db import models
from Accounts.models import User
import secrets
from .paystack import PayStack


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

    def verify_payment(self):
        paystack = PayStack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            self.verified = True
            self.save()
            if self.verified:
                return True
        return False