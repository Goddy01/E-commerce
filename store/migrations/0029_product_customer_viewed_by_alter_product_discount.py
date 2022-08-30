# Generated by Django 4.0.2 on 2022-08-30 00:33

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0002_alter_user_first_phone_num'),
        ('store', '0028_product_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='customer_viewed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_secondary_user', to='Accounts.customer'),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.DecimalField(decimal_places=0, default=Decimal('0'), max_digits=3, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]