# Generated by Django 3.0.6 on 2020-12-21 00:05

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_product_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='color',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('#FFFFFF', 'White'), ('#C0C0C0', 'Sliver'), ('#808080', 'Gray'), ('#000000', 'Black'), ('#FF0000', 'Red'), ('#FFFF00', 'Yellow'), ('#008000', 'Green'), ('#0000FF', 'Blue'), ('#800080', 'Purple')], max_length=71, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='gender',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('male', 'male'), ('female', 'female'), ('kid', 'kid')], max_length=15, null=True),
        ),
    ]