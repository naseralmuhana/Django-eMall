# Generated by Django 3.0.6 on 2020-12-20 22:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20201221_0035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=4, null=True, validators=[django.core.validators.MinValueValidator(0.9)]),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=4, validators=[django.core.validators.MinValueValidator(0.9)]),
        ),
    ]
