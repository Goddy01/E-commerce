from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.



class Vendor_Acct(AbstractBaseUser):
    fullname =                      models.CharField(blank=False, null=False, max_length=256)
    username =                      models.Charfield(blank=False, null=False, max_length=256, unique=True)
    address =                       models.CharField(blank=False, null=False, max_length=512)
    first_phone_number =            PhoneNumberField(null=False, blank=False, verbose_name='first phone number')
    second_phone_number =           PhoneNumberField(null=False, blank=False)