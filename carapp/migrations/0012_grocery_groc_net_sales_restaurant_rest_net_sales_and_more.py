# Generated by Django 4.2 on 2023-05-31 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carapp', '0011_grocery_groc_daily_expenses_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='grocery',
            name='groc_net_sales',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='rest_net_sales',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='grocery',
            name='groc_daily_expenses',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='rest_daily_expenses',
            field=models.IntegerField(null=True),
        ),
    ]
