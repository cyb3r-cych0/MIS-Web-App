import dateutil.utils
from django.db import models
from django.utils import timezone
import datetime


# Create your models here.
class Car(models.Model):
    # ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
    SERVICE_CHOICES = [('Car Wash', 'Car Wash'), ('Car Service', 'Car Service')]
    ADDITIONAL_SERVICES = [('Polishing', 'Polishing'), ('Buffing', 'Buffing'), ('Engine Wash', 'Engine Wash'), ('Under Wash', 'Under Wash')]
    car_model = models.CharField(max_length=100)
    car_number = models.CharField(max_length=30)
    car_notes = models.TextField()
    car_description = models.CharField(max_length=100)
    car_owner_name = models.CharField(max_length=100)
    car_owner_number = models.IntegerField()
    service_type = models.CharField(choices=SERVICE_CHOICES, max_length=15, blank=True, default='Car Wash')
    submission_date = models.DateField(default=dateutil.utils.today())
    servicing = models.CharField(choices=ADDITIONAL_SERVICES, max_length=15, blank=True)
    servicing_cost = models.IntegerField(unique=False, null=True)

    def __str__(self):
        return self.car_model


class Expenses(models.Model):
    # car = models.ForeignKey(Car, on_delete=models.CASCADE)
    expenditure_date = models.DateField(default=dateutil.utils.today())
    daily_commission = models.IntegerField(unique=False, null=False)
    electricity = models.IntegerField(unique=False, null=True)
    misc_expenses = models.IntegerField(unique=False, null=True)
    rent = models.IntegerField(unique=False, null=True)


class Restaurant(models.Model):
    rest_sales_date = models.DateField(default=dateutil.utils.today())
    rest_daily_sales = models.IntegerField(unique=False)

    def __int__(self):
        return self.rest_daily_sales


class RestaurantExpense(models.Model):
    r_expenditure_date = models.DateField(default=dateutil.utils.today())
    r_salary_expenses = models.IntegerField(unique=False, null=True)
    r_misc_expenses = models.IntegerField(unique=False, null=True)


class Grocery(models.Model):
    groc_sales_date = models.DateField(default=dateutil.utils.today())
    groc_daily_sales = models.IntegerField(unique=False)

    def __int__(self):
        return self.groc_daily_sales


class GroceryExpense(models.Model):
    g_expenditure_date = models.DateField(default=dateutil.utils.today())
    g_salary_expenses = models.IntegerField(unique=False, null=True)
    g_misc_expenses = models.IntegerField(unique=False, null=True)
    g_stock_expenses = models.IntegerField(unique=False, null=True)




