from django.contrib import admin
from .models import Car
from .models import Restaurant
from .models import Grocery
from .models import Expenses
from .models import RestaurantExpense
from .models import GroceryExpense


# Register your models here.
# admin.site.register(Car)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['car_model', 'car_number', 'car_notes', 'service_type', 'servicing_cost']
    search_fields = ['car_model', 'car_number', 'car_notes', 'service_type', 'servicing_cost']
    list_per_page = 10


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['rest_sales_date', 'rest_daily_sales']
    search_fields = ['rest_sales_date', 'rest_daily_sales']
    list_per_page = 10


@admin.register(Grocery)
class GroceryAdmin(admin.ModelAdmin):
    list_display = ['groc_sales_date', 'groc_daily_sales']
    search_fields = ['groc_sales_date', 'groc_daily_sales']
    list_per_page = 10


@admin.register(Expenses)
class ExpensesAdmin(admin.ModelAdmin):
    list_display = ['expenditure_date', 'daily_commission', 'electricity', 'misc_expenses', 'rent']
    search_fields = ['expenditure_date', 'daily_commission', 'electricity', 'misc_expenses', 'rent']
    list_per_page = 10


@admin.register(RestaurantExpense)
class RestaurantExpenseAdmin(admin.ModelAdmin):
    list_display = ['r_expenditure_date', 'r_salary_expenses', 'r_misc_expenses']
    search_fields = ['r_expenditure_date', 'r_salary_expenses', 'r_misc_expenses']
    list_per_page = 10


@admin.register(GroceryExpense)
class GroceryExpenseAdmin(admin.ModelAdmin):
    list_display = ['g_expenditure_date', 'g_salary_expenses', 'g_misc_expenses', 'g_stock_expenses']
    search_fields = ['g_expenditure_date', 'g_salary_expenses', 'g_misc_expenses', 'g_stock_expenses']
    list_per_page = 10
