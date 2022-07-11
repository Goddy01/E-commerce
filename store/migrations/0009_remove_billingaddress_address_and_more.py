# Generated by Django 4.0.2 on 2022-07-10 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_order_total_order_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billingaddress',
            name='address',
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='address1',
            field=models.CharField(max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='address2',
            field=models.CharField(max_length=512, null=True),
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='country',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='email',
            field=models.EmailField(max_length=128, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='firstname',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='lastname',
            field=models.CharField(max_length=256, null=True),
        ),
    ]