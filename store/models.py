import uuid
from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_delete

SIZE_CHOICES = (
    ('XS', 'EXTRA SMALL'),
    ('S', 'SMALL'),
    ('M', 'MEDIUM'),
    ('L', 'LARGE'),
    ('XL', 'EXTRA LARGE'),
    ('XXL', 'EXTRA EXTRA LARGE'),
    ('XXXL', 'EXTRA EXTRA EXTRA LARGE'),
)

COLOR_CHOICES = (
    ('green','GREEN'),
    ('blue', 'BLUE'),
    ('red','RED'),
    ('orange','ORANGE'),
    ('black','BLACK'),
    ('white', 'WHITE')
)

def upload_location(instance, filename):
    return f'product/{str(instance.seller)}/{str(instance.product_name)}/{str(instance.product_id)}-{filename}'

# Create your models here.
class AddProduct(models.Model):
    """Creates these fields in the database for a new product."""
    seller =                    models.CharField(max_length=126, blank=False, null=False)
    product_id =                models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True, verbose_name="product's id", blank=False, null=False)
    product_name =              models.CharField(max_length=128, verbose_name="product's name", null=False, blank=False)
    product_price =             models.IntegerField(verbose_name="product's price", null=False, blank=False)
    product_sizes =             models.CharField(max_length=7, choices=SIZE_CHOICES, default='M', null=True, blank=True)
    number_available =          models.IntegerField(verbose_name='number available', null=False, blank=False)
    product_colors =            models.CharField(max_length=10, choices=COLOR_CHOICES, default='green', verbose_name="product's colors", null=False, blank=False)
    product_weight =            models.FloatField(verbose_name="product's weight", null=False, blank=False)
    product_image1 =            models.ImageField(upload_to=upload_location, null=False, blank=False, verbose_name='product image 1', null=False, blank=False)
    product_image2 =            models.ImageField(upload_to=upload_location, null=True, blank=True, verbose_name='product image 2', null=True, blank=True)
    product_image3 =            models.ImageField(upload_to=upload_location, null=True, blank=True, verbose_name='product image 3')
    product_description =       models.TextField(max_length=1000, verbose_name="product's description", null=False, blank=False)
    slug =                      models.SlugField(blank=True, unique=True, max_length=256)

    def __str__(self):
        return self.product_name


def pre_save_product_receiver(sender, instance, **kwargs):
    """Checks if a product has a slug, if not it creates one before committing to the database"""
    if not instance.slug:
        instance.slug = slugify(instance.seller + '-' + instance.product_name + '-' + instance.product_id)
pre_save.connect(pre_save_product_receiver, sender=AddProduct)