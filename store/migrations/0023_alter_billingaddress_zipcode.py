# Generated by Django 4.0.2 on 2022-07-20 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0022_alter_billingaddress_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingaddress',
            name='zipcode',
            field=models.IntegerField(max_length=256),
        ),
    ]
