# Generated by Django 4.0.2 on 2022-08-27 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0002_alter_user_first_phone_num'),
        ('store', '0024_usersrecentlyviewedproduct'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersrecentlyviewedproduct',
            name='user',
        ),
        migrations.AddField(
            model_name='usersrecentlyviewedproduct',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Accounts.customer'),
        ),
    ]
