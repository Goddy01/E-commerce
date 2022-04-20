from django.db import models

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
    file_path = 

# Create your models here.
class AddProduct(models.Model):
    """Creates these fields in the database for a new product."""
    product_name =              models.CharField(max_length=128, verbose_name="product's name")
    product_price =             models.IntegerField(verbose_name="product's price")
    product_sizes =             models.CharField(max_length=7, choices=SIZE_CHOICES, default='M')
    number_available =          models.IntegerField(verbose_name='number available')
    product_colors =            models.CharField(max_length=10, choices=COLOR_CHOICES, default='green', verbose_name="product's colors")
    product_weight =            models.FloatField(verbose_name="product's weight")
    product_image1 =            models.ImageField(upload_to=upload_location, null=True, blank=True, verbose_name='product image 1')
    product_image2 =            models.ImageField(upload_to=upload_location, null=True, blank=True, verbose_name='product image 2')
    product_image3 =            models.ImageField(upload_to=upload_location, null=True, blank=True, verbose_name='product image 3')
    product_description =       models.TextField(max_length=1000, verbose_name="product's description")
    slug =                      models.SlugField(blank=True, unique=True, max_length=256)

    def __str__(self):
        return self.product_name