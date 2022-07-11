import uuid
from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from Accounts.models import Customer
from django_countries.fields import CountryField

def upload_location(instance, filename):
    return f'product/{str(instance.seller)}/{str(instance.product_name)}/{str(instance.product_id)}-{filename}'


class Product(models.Model):
    """Creates these fields in the database for a new product."""
        

    seller =                    models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE, null=True, blank=True)
    product_id =                models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True, verbose_name="product's id", blank=True)
    product_name =              models.CharField(max_length=128, verbose_name="product's name", null=False, blank=False)
    product_price =             models.IntegerField(verbose_name="product's price", null=False, blank=False)
    product_sizes =             models.CharField(max_length=256, null=False, blank=False, verbose_name="product sizes")
    number_available =          models.IntegerField(verbose_name='number available', blank=False, null=False)
    product_colors =            models.CharField(max_length=256,verbose_name="product's colors", blank=False, null=False)
    product_categories =            models.CharField(max_length=256,verbose_name="product's categories", blank=False, null=False)
    # product_category =          models.ManyToManyField(Category)
    # product_weight =            models.FloatField(verbose_name="product's weight", null=False, blank=False)
    product_image1 =            models.ImageField(upload_to=upload_location, null=True, blank=False, verbose_name='product image 1')
    product_image2 =            models.ImageField(upload_to=upload_location, null=True, blank=True, verbose_name='product image 2')
    product_image3 =            models.ImageField(upload_to=upload_location, null=True, blank=True, verbose_name='product image 3')
    product_description =       models.TextField(max_length=1000, verbose_name="product's description", blank=False)
    slug =                      models.SlugField(blank=True, unique=True, max_length=256)

    def __str__(self):
        return self.product_name


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
    customer =              models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    date_ordered =          models.DateTimeField(auto_now_add=True)
    complete =              models.BooleanField(default=False)
    total_order_price =     models.IntegerField(null=True)

    def __str__(self):
        return str(self.transaction_id)

    @property
    def get_cart_total(self):
        orderitems =    self.orderitem_set.all()
        total =         sum([item.get_items_price for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems =          self.orderitem_set.all()
        items_total =         sum([item.quantity for item in orderitems])
        return items_total

    # @property
    # def total_order_price(self):
    #     orderitems =    self.orderitem_set.all()
    #     total_order =   sum([]item.quantity)


class OrderItem(models.Model):
    item_id =       models.UUIDField(default=uuid.uuid4, editable=True, null=True, unique=True)
    order =         models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    product =       models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date_added =    models.DateTimeField(auto_now_add=True)
    quantity =      models.IntegerField(null=True, blank=True, default=0)

    @property
    def get_items_price(self):
        total_item_price = self.quantity * self.product.product_price
        return total_item_price




class BillingAddress(models.Model):
    customer =          models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    firstname =         models.CharField(max_length=256, null=False, default="")
    lastname =          models.CharField(max_length=256, null=False, default="")
    email =             models.EmailField(max_length=128, unique=True, null=False, default="")
    address1 =          models.CharField(max_length=512, null=False, default="")
    address2 =          models.CharField(max_length=512, null=False, default="")
    order =             models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    country =           CountryField(max_length=256, null=False, default="")
    city =              models.CharField(null=False, max_length=256, default="")
    state =             models.CharField(null=False, max_length=256)
    zipcode =           models.CharField(null=False, max_length=256)
    date_added =        models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
