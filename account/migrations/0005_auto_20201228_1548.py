# Generated by Django 3.0.6 on 2020-12-28 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20201228_0158'),
    ]

    operations = [
        migrations.AddField(
            model_name='userregistration',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='User-Profile-Images'),
        ),
        migrations.AlterField(
            model_name='userregistration',
            name='city',
            field=models.CharField(blank=True, choices=[('Amman', 'Amman'), ('Irbid', 'Irbid'), ('Ajloun', 'Ajloun'), ('Jerash', 'Jerash'), ('Mafraq', 'Mafraq'), ('Balqa', 'Balqa'), ('Zarqa', 'Zarqa'), ('Madaba', 'Madaba'), ('Karak', 'Karak'), ('Tafilah', 'Tafilah'), ("Ma'an", "Ma'an"), ('Aqaba', 'Aqaba')], max_length=100, null=True),
        ),
    ]