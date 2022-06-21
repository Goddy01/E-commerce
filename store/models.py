import uuid
from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

def upload_location(instance, filename):
    return f'product/{str(instance.seller)}/{str(instance.product_name)}/{str(instance.product_id)}-{filename}'

# Create your models here.
class Product(models.Model):
    """Creates these fields in the database for a new product."""

    class Color(models.TextChoices):
        """Choices for different colors"""
        GREEN = "GREEN"
        BLUE = "BLUE"
        RED = "RED"
        ORANGE = "ORANGE"
        BLACK = "BLACK"
        WHITE = "WHITE"
        YELLOW = "YELLOW"
        PURPLE = "PURPLE"
        BROWN = "BROWN"
        PINK = "PINK"
    
    class Size(models.TextChoices):
        """Choices for sizes"""
        XS =    "XS", "EXTRA SMALL"
        S =     "S", "SMALL"
        M =     "M", "MEDIUM"
        L =     "L", "LARGE"
        XL =    "XL", "EXTRA LARGE"
        XXL =   "XXL", "EXTRA EXTRA LARGE"
        XXXL =  "XXXL", "EXTRA EXTRA EXTRA LARGE"
    seller =                    models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)
    product_id =                models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True, verbose_name="product's id", blank=True)
    product_name =              models.CharField(max_length=128, verbose_name="product's name", null=False, blank=False)
    product_price =             models.IntegerField(verbose_name="product's price", null=True, blank=False)
    product_sizes =             models.CharField(max_length=7, choices=Size.choices, default=Size.M, null=True, blank=False)
    number_available =          models.IntegerField(verbose_name='number available', blank=False, null=False)
    product_colors =            models.CharField(max_length=10, choices=Color.choices, default=Color.WHITE, verbose_name="product's colors", blank=False)
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
        instance.slug = slugify(instance.seller + '-' + instance.product_name + '-' + f"{instance.product_id}")
pre_save.connect(pre_save_product_receiver, sender=Product)


@receiver(post_delete, sender=Product)
def submission_delete(sender, instance, **kwargs):
    """Deletes the image(s) of a product when the correlating product is deleted"""
    instance.product_image1.delete(False)
    instance.product_image2.delete(False)
    instance.product_image3.delete(False)