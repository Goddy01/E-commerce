# Generated by Django 4.0.2 on 2022-09-05 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0030_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlist',
            name='heart_val',
            field=models.BooleanField(default=False),
        ),
    ]
