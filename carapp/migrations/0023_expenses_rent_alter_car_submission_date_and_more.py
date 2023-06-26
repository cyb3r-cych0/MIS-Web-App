# Generated by Django 4.2 on 2023-06-23 09:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carapp', '0022_alter_car_submission_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenses',
            name='rent',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='car',
            name='submission_date',
            field=models.DateField(default=datetime.datetime(2023, 6, 23, 0, 0)),
        ),
        migrations.AlterField(
            model_name='expenses',
            name='expenditure_date',
            field=models.DateField(default=datetime.datetime(2023, 6, 23, 0, 0)),
        ),
        migrations.AlterField(
            model_name='grocery',
            name='groc_sales_date',
            field=models.DateField(default=datetime.datetime(2023, 6, 23, 0, 0)),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='rest_sales_date',
            field=models.DateField(default=datetime.datetime(2023, 6, 23, 0, 0)),
        ),
    ]