# Generated by Django 3.0.6 on 2021-01-05 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('In Progress', 'In Progress'), ('Canceled', 'Canceled'), ('Delayed', 'Delayed'), ('Delivered', 'Delivered')], default='In Progress', max_length=15),
        ),
    ]
