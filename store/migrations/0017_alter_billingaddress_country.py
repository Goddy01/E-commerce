# Generated by Django 4.0.2 on 2022-07-20 00:59

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_rename_first_phone_num_billingaddress_phone_num1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingaddress',
            name='country',
            field=django_countries.fields.CountryField(max_length=256),
        ),
    ]