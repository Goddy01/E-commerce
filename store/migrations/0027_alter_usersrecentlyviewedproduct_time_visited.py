# Generated by Django 4.0.2 on 2022-08-27 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0026_alter_product_last_visit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersrecentlyviewedproduct',
            name='time_visited',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]