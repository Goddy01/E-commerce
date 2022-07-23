# Generated by Django 4.0.2 on 2022-07-23 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0024_alter_billingaddress_zipcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name="product's price"),
        ),
    ]
