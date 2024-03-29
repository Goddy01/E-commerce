# Generated by Django 4.0.2 on 2022-09-14 00:59

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import phonenumber_field.modelfields
import store.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_id', models.UUIDField(default=uuid.uuid4, null=True)),
                ('date_ordered', models.DateTimeField(auto_now_add=True)),
                ('complete', models.BooleanField(default=False)),
                ('total_order_price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Accounts.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.UUIDField(blank=True, default=uuid.uuid4, primary_key=True, serialize=False, verbose_name="product's id")),
                ('product_name', models.CharField(max_length=128, verbose_name="product's name")),
                ('product_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name="product's price")),
                ('product_sizes', models.CharField(max_length=256, verbose_name='product sizes')),
                ('number_available', models.IntegerField(verbose_name='number available')),
                ('product_colors', models.CharField(max_length=256, verbose_name="product's colors")),
                ('product_categories', models.CharField(max_length=256, verbose_name="product's categories")),
                ('product_image1', models.ImageField(null=True, upload_to=store.models.upload_location, verbose_name='product image 1')),
                ('product_image2', models.ImageField(blank=True, null=True, upload_to=store.models.upload_location, verbose_name='product image 2')),
                ('product_image3', models.ImageField(blank=True, null=True, upload_to=store.models.upload_location, verbose_name='product image 3')),
                ('product_description', models.TextField(max_length=1000, verbose_name="product's description")),
                ('slug', models.SlugField(blank=True, max_length=256, unique=True)),
                ('num_of_reviews', models.IntegerField(blank=True, null=True)),
                ('average_rating', models.IntegerField(blank=True, null=True)),
                ('num_of_ratings', models.IntegerField(blank=True, null=True)),
                ('num_of_visits', models.IntegerField(blank=True, default=0, null=True)),
                ('last_visit', models.DateTimeField(auto_now=True, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True, null=True)),
                ('discount', models.DecimalField(decimal_places=0, default=Decimal('0'), max_digits=3, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('customer_viewed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_secondary_user', to='Accounts.customer')),
                ('seller', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.UUIDField(default=uuid.uuid4, null=True, unique=True)),
                ('date_added', models.DateTimeField()),
                ('heart_val', models.BooleanField(default=False)),
                ('wish_item_counter', models.IntegerField(null=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Accounts.customer')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
        migrations.CreateModel(
            name='UsersRecentlyViewedProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_visited', models.DateTimeField(blank=True, null=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Accounts.customer')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_review', models.TextField(blank=True, max_length=1000, null=True)),
                ('rating', models.IntegerField(blank=True, default=0, null=True)),
                ('created_on', models.DateTimeField(blank=True, null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Accounts.customer')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.UUIDField(default=uuid.uuid4, null=True, unique=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('size', models.CharField(max_length=10, null=True)),
                ('color', models.CharField(max_length=10, null=True)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.order')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
        migrations.CreateModel(
            name='BillingAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(blank=True, default='', max_length=256)),
                ('country', django_countries.fields.CountryField(max_length=256)),
                ('phone_num1', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region='', verbose_name='Phone No 1')),
                ('email', models.EmailField(default='', max_length=128)),
                ('address', models.CharField(blank=True, default='', max_length=512)),
                ('city', models.CharField(default='', max_length=256)),
                ('state', models.CharField(max_length=256)),
                ('zipcode', models.IntegerField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Accounts.customer')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.order')),
            ],
        ),
    ]
