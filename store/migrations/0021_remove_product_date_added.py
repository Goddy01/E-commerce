# Generated by Django 4.0.2 on 2022-08-27 14:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0020_product_date_added'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='date_added',
        ),
    ]
