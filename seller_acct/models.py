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
    date_joined             = models.DateTimeField(auto_now_add=True)
    last_login              = models.DateTimeField(auto_now=True)
    is_admin                = models.BooleanField(default=False)
    is_staff                = models.BooleanField(default=False)
    is_active               = models.BooleanField(default=True)
    is_superuser            = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    # objects = 

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        """Checks if the user has any permissions"""
        return self.is_admin

    def has_module_perms(self, app_label):
        """Checks if the user has permission to view the app 'app_label'"""
        return True