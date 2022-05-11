# Generated by Django 4.0.2 on 2022-05-11 21:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor_Acct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('fullname', models.CharField(max_length=256)),
                ('username', models.CharField(max_length=256, unique=True)),
                ('address', models.CharField(max_length=512)),
                ('first_phone_num', models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+123456789'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='first phone num')),
                ('second_phone_num', models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+123456789'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='second phone num')),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
