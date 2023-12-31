# Generated by Django 4.2 on 2023-06-21 12:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carapp', '0020_alter_car_submission_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='submission_date',
            field=models.DateField(verbose_name=datetime.datetime(2023, 6, 21, 12, 21, 19, 498031, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='expenses',
            name='expenditure_date',
            field=models.DateField(verbose_name=datetime.datetime(2023, 6, 21, 12, 21, 19, 500200, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='grocery',
            name='groc_sales_date',
            field=models.DateField(verbose_name=datetime.datetime(2023, 6, 21, 12, 21, 19, 499339, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='rest_sales_date',
            field=models.DateField(verbose_name=datetime.datetime(2023, 6, 21, 12, 21, 19, 498818, tzinfo=datetime.timezone.utc)),
        ),
    ]
