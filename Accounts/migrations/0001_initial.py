# Generated by Django 4.0.2 on 2022-09-14 00:55

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('fullname', models.CharField(max_length=256)),
                ('username', models.CharField(max_length=256, unique=True)),
                ('email', models.EmailField(max_length=128, unique=True)),
                ('address', models.CharField(max_length=512)),
                ('first_phone_num', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='Phone No 1')),
                ('device', models.CharField(max_length=256)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('type', models.CharField(choices=[('VENDOR', 'Vendor'), ('CUSTOMER', 'Customer')], default='CUSTOMER', max_length=50, verbose_name='Type')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('Accounts.user',),
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('Accounts.user',),
        ),
    ]
