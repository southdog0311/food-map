# Generated by Django 4.2.15 on 2024-08-16 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0003_remove_place_opening_hours_place_closing_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='photo',
            field=models.ImageField(blank=True, help_text='Upload a photo', null=True, upload_to='photos/'),
        ),
    ]
