# Generated by Django 4.0.2 on 2022-06-21 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_alter_product_number_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_sizes',
            field=models.CharField(choices=[('XS', 'EXTRA SMALL'), ('S', 'SMALL'), ('M', 'MEDIUM'), ('L', 'LARGE'), ('XL', 'EXTRA LARGE'), ('XXL', 'EXTRA EXTRA LARGE'), ('XXXL', 'EXTRA EXTRA EXTRA LARGE')], default='M', max_length=7, null=True),
        ),
    ]
