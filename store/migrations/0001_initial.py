# Generated by Django 4.0.2 on 2022-06-22 18:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import store.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.UUIDField(blank=True, default=uuid.uuid4, primary_key=True, serialize=False, verbose_name="product's id")),
                ('product_name', models.CharField(max_length=128, verbose_name="product's name")),
                ('product_price', models.IntegerField(null=True, verbose_name="product's price")),
                ('number_available', models.IntegerField(verbose_name='number available')),
                ('product_colors', models.CharField(max_length=12, verbose_name="product's colors")),
                ('product_image1', models.ImageField(null=True, upload_to=store.models.upload_location, verbose_name='product image 1')),
                ('product_image2', models.ImageField(blank=True, null=True, upload_to=store.models.upload_location, verbose_name='product image 2')),
                ('product_image3', models.ImageField(blank=True, null=True, upload_to=store.models.upload_location, verbose_name='product image 3')),
                ('product_description', models.TextField(max_length=1000, verbose_name="product's description")),
                ('slug', models.SlugField(blank=True, max_length=256, unique=True)),
                ('seller', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
