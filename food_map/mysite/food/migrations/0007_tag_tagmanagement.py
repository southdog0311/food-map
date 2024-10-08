# Generated by Django 4.2.15 on 2024-08-28 09:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0006_alter_place_photo_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('Rstyle', models.CharField(max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TagManagement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='food.place')),
                ('tag', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='food.tag')),
            ],
        ),
    ]
