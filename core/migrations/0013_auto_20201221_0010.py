# Generated by Django 3.0.6 on 2020-12-20 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20201221_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='Products-images/<django.db.models.fields.related.ForeignKey>/'),
        ),
    ]
