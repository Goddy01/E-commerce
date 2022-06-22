import uuid
from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

def upload_location(instance, filename):
    return f'product/{str(instance.seller)}/{str(instance.product_name)}/{str(instance.product_id)}-{filename}'


class Product(models.Model):
    """Creates these fields in the database for a new product."""

    class Color(models.TextChoices):
        """Choices for different colors"""
        

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