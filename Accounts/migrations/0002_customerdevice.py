# Generated by Django 4.0.2 on 2022-07-27 16:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerDevice',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('device', models.CharField(blank=True, max_length=256, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('Accounts.customer',),
        ),
    ]
