import uuid
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from Accounts.models import Customer, User
from django_countries.fields import CountryField
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

def upload_location(instance, filename):
    return f'product/{str(instance.seller)}/{str(instance.product_name)}/{str(instance.product_id)}-{filename}'

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]
class Product(models.Model):
    """Creates these fields in the database for a new product."""

    seller =                    models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE, null=True, blank=True)
    product_id =                models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True, verbose_name="product's id", blank=True)
    product_name =              models.CharField(max_length=128, verbose_name="product's name", null=False, blank=False)
    product_price =             models.DecimalField(max_digits=255, decimal_places=2, verbose_name="product's price", null=False, blank=False)
    product_sizes =             models.CharField(max_length=255, null=False, blank=False, verbose_name="product sizes")
    number_available =          models.IntegerField(verbose_name='number available', blank=False, null=False)
    product_colors =            models.CharField(max_length=255,verbose_name="product's colors", blank=False, null=False)
    product_categories =            models.CharField(max_length=255,verbose_name="product's categories", blank=False, null=False)
    # product_category =          models.ManyToManyField(Category)
    # product_weight =            models.FloatField(verbose_name="product's weight", null=False, blank=False)
    product_image1 =            models.ImageField(upload_to=upload_location, null=True, blank=False, verbose_name='product image 1')
    product_image2 =            models.ImageField(upload_to=upload_location, null=True, blank=True, verbose_name='product image 2')
    product_image3 =            models.ImageField(upload_to=upload_location, null=True, blank=True, verbose_name='product image 3')
    product_description =       models.TextField(max_length=1000, verbose_name="product's description", blank=False)
    slug =                      models.SlugField(blank=True, unique=True, max_length=255)
    num_of_reviews =            models.IntegerField(blank=True, null=True)
    average_rating =            models.IntegerField(blank=True, null=True)
    num_of_ratings =            models.IntegerField(blank=True, null=True)
    num_of_visits =             models.IntegerField(blank=True, null=True, default=0)
    last_visit =                models.DateTimeField(auto_now=True, blank=True, null=True)
    date_added =                models.DateTimeField(auto_now_add=True, null=True, blank=True)
    discount =                  models.DecimalField(max_digits=3, decimal_places=0, default=Decimal(0), validators=PERCENTAGE_VALIDATOR, null=True, blank=False)
    customer_viewed_by =        models.ForeignKey(Customer, related_name='related_secondary_user', on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.product_name

    @property
    def get_discount_price(self):
        discount_price = self.product_price - (self.product_price * self.discount)/100
        return discount_price

class UsersRecentlyViewedProduct(models.Model):
    customer =          models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    product =       models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    time_visited =  models.DateTimeField(blank=True, null=True)

    def __str__(self):
        if self.customer is not None:
            return self.customer.fullname
        else:
            return ''

def pre_save_product_receiver(sender, instance, **kwargs):
    """Checks if a product has a slug, if not it creates one before committing to the database"""
    if not instance.slug:
        instance.slug = slugify(f"{instance.seller}" + '-' + f"{instance.product_name}" + '-' + f"{instance.product_id}")
pre_save.connect(pre_save_product_receiver, sender=Product)


@receiver(post_delete, sender=Product)
def submission_delete(sender, instance, **kwargs):
    """Deletes the image(s) of a product when the correlating product is deleted"""
    instance.product_image1.delete(False)
    instance.product_image2.delete(False)
    instance.product_image3.delete(False)


class Order(models.Model):
    transaction_id =        models.UUIDField(default=uuid.uuid4, editable=True, null=True)
    customer =              models.ForeignKey(Customer, null=True, blank=True, on_delete=models.CASCADE)
    date_ordered =          models.DateTimeField(auto_now_add=True)
    complete =              models.BooleanField(default=False)
    total_order_price =     models.DecimalField(max_digits=255, decimal_places=2, null=True)


    @property
    def get_cart_total(self):
        orderitems =    self.orderitem_set.all()
        total =         sum([item.get_items_price for item in orderitems])
        return total

    @get_cart_total.setter
    def get_cart_total(self, value):
        pass

    @property
    def get_cart_items(self):
        orderitems =          self.orderitem_set.all()
        items_total =         sum([item.quantity for item in orderitems])
        return items_total

    # @property
    # def total_order_price(self):
    #     orderitems =    self.orderitem_set.all()
    #     total_order =   sum([]item.quantity)
    @property
    def shipping(self):
        shipping = True
        return shipping

    def __str__(self):
        return str(self.transaction_id)


class Review(models.Model):
    product =     models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    user =        models.ForeignKey(Customer, on_delete=models.CASCADE, null=False)
    user_review = models.TextField(max_length=1000, blank=True, null=True)
    rating =      models.IntegerField(null=True, default=0, blank=True)
    created_on =  models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.fullname}'s review"


class OrderItem(models.Model):
    item_id =               models.UUIDField(default=uuid.uuid4, editable=True, null=True, unique=True)
    order =                 models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product =               models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    date_added =            models.DateTimeField(auto_now_add=True)
    quantity =              models.IntegerField(null=True, blank=True, default=0)
    size =                 models.CharField(max_length=255, null=True, blank=False)
    color =                 models.CharField(max_length=255, null=True, blank=False)
    
    @property
    def ordered_product_color(self):
        return self.product.product_colors.split(',')
    # p = self.OrderItem()
    # opc = p.ordered_product_color()
    # for color in opc:
    #     COLOR_CHOICES.append((color, color))
    @property
    def ordered_product_size(self):
        return self.product.product_sizes.split(',')
    

    @property
    def get_items_price(self):
        total_item_price = self.quantity * self.product.get_discount_price
        return total_item_price

    @get_items_price.setter
    def get_items_price(self, value):
        # self._location = value
        pass


class WishList(models.Model):
    item_id =           models.UUIDField(default=uuid.uuid4, editable=True, null=True, unique=True)
    customer =          models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    product =           models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    date_added =        models.DateTimeField(auto_now_add=True)
    heart_val =         models.BooleanField(default=False)
    wish_item_counter = models.IntegerField(null=True, blank=False)

    def __str__(self):
        return f'{self.customer.username}-{self.product.product_name}'


class BillingAddress(models.Model):
    customer =          models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    fullname =         models.CharField(max_length=255, null=False, default="", blank=True)
    country =           CountryField(max_length=255, null=False, blank=False)
    phone_num1 =        PhoneNumberField(null=True, blank=True, verbose_name="Phone No 1", region="")
    email =             models.EmailField(max_length=128, null=False, default="", blank=False)
    address =          models.CharField(max_length=512, null=False, default="", blank=True)
    order =             models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    city =              models.CharField(null=False, max_length=255, default="", blank=False)
    state =             models.CharField(null=False, max_length=255, blank=False)
    zipcode =           models.IntegerField(null=False, blank=False)
    date_added =        models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f' {self.fullname}, {self.customer.username}, ({self.address})'
