# Generated by Django 4.2.4 on 2023-09-23 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppTravel', '0004_alter_travel_cities_alter_travel_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='message',
            field=models.CharField(max_length=800),
        ),
        migrations.AlterField(
            model_name='tours',
            name='text',
            field=models.CharField(max_length=800),
        ),
        migrations.AlterField(
            model_name='travel',
            name='description',
            field=models.CharField(max_length=500),
        ),
    ]