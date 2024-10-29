# Generated by Django 5.1.2 on 2024-10-28 21:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0006_remove_ingredient_stock_stock_ingredient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='ingredient',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='stock', to='restaurant.ingredient'),
        ),
    ]
