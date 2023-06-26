from django import forms
from django.forms import ModelForm
from .models import Car
from .models import Restaurant
from .models import Grocery
from .models import Expenses
from .models import RestaurantExpense, GroceryExpense
from django.core.validators import RegexValidator


class CarForm(ModelForm):

    # Validations
    car_model = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Example: BMW'}),
        min_length=3, max_length=20)
    car_number = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Example: KAE 677S'}),
        min_length=3, max_length=10)
    car_owner_name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Example: John Doe'}),
        min_length=3, max_length=20)
    car_owner_number = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Example: 0700 000 000'}),
        min_length=3, max_length=20)
    car_description = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Example: White SUV'}),
        min_length=3, max_length=15)
    car_notes = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Example: Full Wash'}),
        min_length=3, max_length=20)
    servicing_cost = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Example: 500'}),
        min_length=3, max_length=20)

    class Meta:
        model = Car
        fields = "__all__"

        # Outside Widgets
        widgets = {
            'car_model': forms.TextInput(
                attrs={
                    'style': 'font-size: 30px',
                    'data-mask': '(0000) 000-000'
                }
            )
        }


class GroceryForm(ModelForm):
    groc_daily_sales = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Income: Cash @ Hand In KSH'}),
        min_length=3, max_length=10)

    class Meta:
        model = Grocery
        fields = "__all__"


class RestaurantForm(ModelForm):
    rest_daily_sales = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Income: Cash @ Hand In KSH'}),
        min_length=3, max_length=10)

    class Meta:
        model = Restaurant
        fields = "__all__"


class ExpensesForm(ModelForm):
    daily_commission = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Daily Commission: Based on Washed Cars'}),
        min_length=1, max_length=10)
    electricity = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Electricity: Weekly 100'}),
        min_length=1, max_length=10)
    misc_expenses = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Daily Misc: Soap, Services etc'}),
        min_length=1, max_length=10)
    rent = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Monthly Rent: 10000'}),
        min_length=1, max_length=10)

    class Meta:
        model = Expenses
        fields = "__all__"


class RestaurantExpenseForm(ModelForm):
    r_salary_expenses = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Weekly Salary/Commission: 0'}),
        min_length=1, max_length=10)
    r_misc_expenses = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Misc. Expenses: 0'}),
        min_length=1, max_length=10)

    class Meta:
        model = RestaurantExpense
        fields = "__all__"


class GroceryExpenseForm(ModelForm):
    g_salary_expenses = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Salary/Commission: 0'}),
        min_length=1, max_length=10)
    g_misc_expenses = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Misc. Expenses: 0'}),
        min_length=1, max_length=10)
    g_stock_expenses = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Stock Expenses: 0'}),
        min_length=1, max_length=10)

    class Meta:
        model = GroceryExpense
        fields = "__all__"
