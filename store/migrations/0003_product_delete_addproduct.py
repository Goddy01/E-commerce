# Generated by Django 4.0.2 on 2022-06-20 13:37

from django.db import migrations, models
import store.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_addproduct_product_colors'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('seller', models.CharField(max_length=126)),
                ('product_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name="product's id")),
                ('product_name', models.CharField(max_length=128, verbose_name="product's name")),
                ('product_price', models.IntegerField(verbose_name="product's price")),
                ('product_sizes', models.CharField(choices=[('XS', 'EXTRA SMALL'), ('S', 'SMALL'), ('M', 'MEDIUM'), ('L', 'LARGE'), ('XL', 'EXTRA LARGE'), ('XXL', 'EXTRA EXTRA LARGE'), ('XXXL', 'EXTRA EXTRA EXTRA LARGE')], default='M', max_length=7)),
                ('number_available', models.IntegerField(verbose_name='number available')),
                ('product_colors', models.CharField(choices=[('GREEN', 'Green'), ('BLUE', 'Blue'), ('RED', 'Red'), ('ORANGE', 'Orange'), ('BLACK', 'Black'), ('WHITE', 'White'), ('YELLOW', 'Yellow'), ('PURPLE', 'Purple'), ('BROWN', 'Brown'), ('PINK', 'Pink')], default='WHITE', max_length=10, verbose_name="product's colors")),
                ('product_image1', models.ImageField(upload_to=store.models.upload_location, verbose_name='product image 1')),
                ('product_image2', models.ImageField(blank=True, null=True, upload_to=store.models.upload_location, verbose_name='product image 2')),
                ('product_image3', models.ImageField(blank=True, null=True, upload_to=store.models.upload_location, verbose_name='product image 3')),
                ('product_description', models.TextField(max_length=1000, verbose_name="product's description")),
                ('slug', models.SlugField(blank=True, max_length=256, unique=True)),
            ],
        ),
        migrations.DeleteModel(
            name='AddProduct',
        ),
    ]
