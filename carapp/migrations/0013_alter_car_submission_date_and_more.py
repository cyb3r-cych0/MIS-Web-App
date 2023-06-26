# Generated by Django 4.2 on 2023-06-13 08:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carapp', '0012_grocery_groc_net_sales_restaurant_rest_net_sales_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='submission_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='grocery',
            name='groc_sales_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='rest_sales_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
