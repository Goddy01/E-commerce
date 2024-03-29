from enum import unique
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import RegexValidator
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class AccountManager(BaseUserManager):
    """Creates and saves a user with the given details"""
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("The user must provide an email")
        if not username:
            raise ValueError("The user must provide a username")
        # if not fullname:
        #     raise ValueError("The user must provide their fullname")
        # if not address:
        #     raise ValueError("The user must provide an address")
        # if not first_phone_num:
        #     raise ValueError("The user must provide their first telephone number")
        # if not second_phone_num:
        #     raise ValueError("The user must provide their second telephone number")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            # fullname=fullname,
            # address=address,
            # first_phone_num=first_phone_num,
            # second_phone_num=second_phone_num,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """Creates and saves a superuser with the given details"""
        user = self.create_user(
            email=email,
            username=username,
            # fullname=fullname,
            # address=address,
            # first_phone_num=first_phone_num,
            # second_phone_num=second_phone_num,
            password=password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)


class User(AbstractBaseUser):

    fullname =                      models.CharField(max_length=256)
    username =                      models.CharField(max_length=256, unique=True)
    email =                         models.EmailField(max_length=128, unique=True)
    address =                       models.CharField(max_length=512)
    # phone_regex =                   RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+123456789'. Up to 15 digits allowed.")
    first_phone_num =            PhoneNumberField(null=False, blank=True, verbose_name="Phone No 1")
    # second_phone_num =           PhoneNumberField(null=False, blank=True, unique=True, verbose_name= "Phone No 2")
    device =                        models.CharField(max_length=256, null=False, blank=False)
    date_joined =                   models.DateTimeField(auto_now_add=True)
    last_login =                    models.DateTimeField(auto_now=True)
    is_admin =                      models.BooleanField(default=False)
    is_staff =                      models.BooleanField(default=False)
    is_active =                     models.BooleanField(default=True)
    is_superuser =                  models.BooleanField(default=False)
    # is_vendor               = models.BooleanField(default=False)
    # is_customer             = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    objects = AccountManager()

    def __str__(self):
        if self.username:
            name = self.username
        else:
            name = self.device
        return str(name)

    def has_perm(self, perm, obj=None):
        """Checks if the user has any permissions"""
        return self.is_admin

    def has_module_perms(self, app_label):
        """Checks if the user has permission to view the app 'app_label'"""
        return True

    class Types(models.TextChoices):
        VENDOR = "VENDOR", "Vendor"
        CUSTOMER = "CUSTOMER", "Customer"

    type =                          models.CharField(max_length=50, default=Types.CUSTOMER, choices=Types.choices, verbose_name='Type')

class VendorManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        # User.is_vendor = True
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.VENDOR)

class CustomerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        # User.is_customer = True
        return super().get_queryset(*args, **kwargs).filter(type=User.Types.CUSTOMER)

class Vendor(User):
    objects = VendorManager()
    class Meta:
        proxy = True
        
    def save(self, *args, **kwargs):
        if not self.pk:
            # User.is_vendor = True
            self.type = User.Types.VENDOR
        return super().save(*args, **kwargs)

# class AddCustomer(User):
    

class Customer(User):
    objects = CustomerManager()
    class Meta:
        proxy = True
    def save(self, *args, **kwargs):
        if not self.pk:
            # User.is_customer = True
            self.type = User.Types.CUSTOMER
        return super().save(*args, **kwargs)