# Generated by Django 4.2 on 2023-06-21 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carapp', '0014_expenses'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenses',
            name='electricity',
            field=models.IntegerField(null=True),
        ),
    ]