from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import RegexValidator
# Create your models here.



class Vendor_Acct(AbstractBaseUser):
    fullname =                      models.CharField(blank=False, null=False, max_length=256)
    username =                      models.CharField(blank=False, null=False, max_length=256, unique=True)
    address =                       models.CharField(blank=False, null=False, max_length=512)
    phone_regex =                   RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+123456789'. Up to 15 digits allowed.")
    first_phone_num =            models.CharField(validators=[phone_regex], max_length=17, blank=False, null=False, verbose_name='first phone num') # Validators should be a list
    second_phone_num =           models.CharField(validators=[phone_regex], max_length=17, blank=False, null=False, verbose_name='second phone num') # Validators should be a list