# Generated by Django 3.0.6 on 2020-12-28 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20201228_2347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userregistration',
            name='phone_number',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Phone Number'),
        ),
    ]