# Generated by Django 4.0.2 on 2022-09-09 12:33

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0035_alter_review_created_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingaddress',
            name='phone_num1',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region='', verbose_name='Phone No 1'),
        ),
    ]