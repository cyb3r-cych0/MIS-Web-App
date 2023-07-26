from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required  # Login required to access privates pages
from django.views.decorators.cache import cache_control  # prevent back button(destroy last section)
from django.http import HttpResponse, Http404
from .models import Car, Restaurant, Grocery
from .models import Expenses, RestaurantExpense, GroceryExpense
from .forms import CarForm, RestaurantForm, GroceryForm
from .forms import ExpensesForm, RestaurantExpenseForm, GroceryExpenseForm
from django.contrib import messages
import csv
from django.db.models import Avg
from datetime import datetime
import datetime
from django.db.models import Sum, F, Count, ExpressionWrapper, DecimalField
from django.db.models.functions import TruncMonth, TruncDay, TruncWeek

# Functions to access path
"""Functions To Handle Frontend Requests"""


# Frontend
def frontend(request):
    return render(request, 'frontend.html')


# frontend HTML
def carwash(request):
    return render(request, 'frontend/carwash.html')


# frontend HTML
def rest(request):
    return render(request, 'frontend/rest.html')


# frontend HTML
def groceries(request):
    return render(request, 'frontend/groceries.html')


"""Functions To Handle Backend Requests"""


# Backend
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def backend(request):
    return render(request, 'backend.html')


# display recent cars (backend)
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def car_wash(request):
    # get gross income
    now = datetime.datetime.now()
    cars_all = Car.objects.all()
    total_income = sum(cars_all.values_list('servicing_cost', flat=True))
    # get all expenses
    expenses_all = Expenses.objects.all()
    commissioning_expenses = sum(expenses_all.values_list('daily_commission', flat=True))
    electricity_expenses = sum(expenses_all.values_list('electricity', flat=True))
    misc_expenses = sum(expenses_all.values_list('misc_expenses', flat=True))
    rent_expenses = sum(expenses_all.values_list('rent', flat=True))
    # calculate net income
    sum_expenses = int(commissioning_expenses) + int(electricity_expenses) + int(misc_expenses) + int(rent_expenses)
    net_value = int(total_income) - int(sum_expenses)
    context = {
        'cars_all': cars_all,
        'year': now.year,
        'month': now.strftime('%B'),
        # 'net_value': net_value,
        'sum_expenses': sum_expenses,
        'rent_expenses': rent_expenses
    }
    return render(request, 'backend/car_wash.html', context)


# car wash statistics
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def carwash_statistics(request):
    is_superuser = request.user.is_superuser
    now = datetime.datetime.now()
    # get gross income
    all_cars = Car.objects.all()
    total_income = sum(all_cars.values_list('servicing_cost', flat=True))
    # get all expenses
    all_expenses = Expenses.objects.all()
    commissioning_expenses = sum(all_expenses.values_list('daily_commission', flat=True))
    electricity_expenses = sum(all_expenses.values_list('electricity', flat=True))
    misc_expenses = sum(all_expenses.values_list('misc_expenses', flat=True))
    rent_expenses = sum(all_expenses.values_list('rent', flat=True))

    # calculate net income
    sum_expenses = int(commissioning_expenses) + int(electricity_expenses) + int(misc_expenses) + int(rent_expenses)
    net_value = int(total_income) - int(sum_expenses)
    # get latest monthly, weekly & daily income
    monthly_income = Car.objects.annotate(month=TruncMonth('submission_date')).values('month').annotate(
        total_amount=Sum('servicing_cost'))
    weekly_income = Car.objects.annotate(week=TruncWeek('submission_date')).values('week').annotate(
        total_amount=Sum('servicing_cost'))
    daily_income = Car.objects.annotate(day=TruncDay('submission_date')).values('day').annotate(
        total_amount=Sum('servicing_cost'))
    # get latest monthly, weekly & daily expense
    monthly_commission = Expenses.objects.annotate(month=TruncMonth('expenditure_date')).values('month').annotate(
        total_expense=Sum('daily_commission'))
    monthly_electricity = Expenses.objects.annotate(month=TruncMonth('expenditure_date')).values('month').annotate(
        total_expense=Sum('electricity'))
    monthly_misc_expenses = Expenses.objects.annotate(month=TruncMonth('expenditure_date')).values('month').annotate(
        total_expense=Sum('misc_expenses'))
    monthly_rent = Expenses.objects.annotate(month=TruncMonth('expenditure_date')).values('month').annotate(
        total_expense=Sum('rent'))

    weekly_commission = Expenses.objects.annotate(week=TruncWeek('expenditure_date')).values('week').annotate(
        total_expense=Sum('daily_commission'))
    weekly_electricity = Expenses.objects.annotate(week=TruncWeek('expenditure_date')).values('week').annotate(
        total_expense=Sum('electricity'))
    weekly_misc_expenses = Expenses.objects.annotate(week=TruncWeek('expenditure_date')).values('week').annotate(
        total_expense=Sum('misc_expenses'))

    daily_commission = Expenses.objects.annotate(day=TruncDay('expenditure_date')).values('day').annotate(
        total_expense=Sum('daily_commission'))
    daily_electricity = Expenses.objects.annotate(day=TruncDay('expenditure_date')).values('day').annotate(
        total_expense=Sum('electricity'))
    daily_misc_expenses = Expenses.objects.annotate(day=TruncDay('expenditure_date')).values('day').annotate(
        total_expense=Sum('misc_expenses'))

    context = {
        # 'year': now.year,
        # 'month': now.strftime('%B'),
        # 'week': now.isoweekday(),
        # 'day': now.today(),
        'total_income': total_income,
        'sum_expenses': sum_expenses,
        'net_value': net_value,
        'monthly_income': monthly_income,
        'weekly_income': weekly_income,
        'daily_income': daily_income,
        'monthly_commission': monthly_commission,
        'monthly_electricity': monthly_electricity,
        'monthly_misc_expenses': monthly_misc_expenses,
        'is_superuser': is_superuser,
        # 'weekly_commission': weekly_commission,
        # 'weekly_electricity': weekly_electricity,
        # 'weekly_misc_expenses': weekly_misc_expenses,
        # 'daily_commission': daily_commission,
        # 'daily_electricity': daily_electricity,
        # 'daily_misc_expenses': daily_misc_expenses,
        'monthly_rent': monthly_rent
    }
    return render(request, 'carwash/carwash_statistics.html', context)


# restaurant statistics
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def restaurant_statistics(request):
    is_superuser = request.user.is_superuser
    # get gross income
    all_restaurant = Restaurant.objects.all()
    total_income = sum(all_restaurant.values_list('rest_daily_sales', flat=True))

    all_expenses = RestaurantExpense.objects.all()
    salary_expenses = sum(all_expenses.values_list('r_salary_expenses', flat=True))
    misc_expenses = sum(all_expenses.values_list('r_misc_expenses', flat=True))

    # calculate net income
    sum_expenses = int(salary_expenses) + int(misc_expenses)
    net_value = int(total_income) - int(sum_expenses)

    # get latest monthly, weekly & daily income
    monthly_income = Restaurant.objects.annotate(month=TruncMonth('rest_sales_date')).values('month').annotate(
        total_amount=Sum('rest_daily_sales'))
    weekly_income = Restaurant.objects.annotate(week=TruncWeek('rest_sales_date')).values('week').annotate(
        total_amount=Sum('rest_daily_sales'))
    daily_income = Restaurant.objects.annotate(day=TruncDay('rest_sales_date')).values('day').annotate(
        total_amount=Sum('rest_daily_sales'))
    # get latest monthly, weekly & daily expense
    monthly_salary = RestaurantExpense.objects.annotate(month=TruncMonth('r_expenditure_date')).values(
        'month').annotate(
        total_expense=Sum('r_salary_expenses'))
    monthly_misc_expenses = RestaurantExpense.objects.annotate(month=TruncMonth('r_expenditure_date')).values(
        'month').annotate(
        total_expense=Sum('r_misc_expenses'))

    weekly_salary = RestaurantExpense.objects.annotate(week=TruncWeek('r_expenditure_date')).values('week').annotate(
        total_expense=Sum('r_salary_expenses'))
    weekly_misc_expenses = RestaurantExpense.objects.annotate(week=TruncWeek('r_expenditure_date')).values(
        'week').annotate(
        total_expense=Sum('r_misc_expenses'))

    daily_salary = RestaurantExpense.objects.annotate(day=TruncDay('r_expenditure_date')).values('day').annotate(
        total_expense=Sum('r_salary_expenses'))
    daily_misc_expenses = RestaurantExpense.objects.annotate(day=TruncDay('r_expenditure_date')).values('day').annotate(
        total_expense=Sum('r_misc_expenses'))

    context = {
        'total_income': total_income,
        'sum_expenses': sum_expenses,
        'net_value': net_value,
        'monthly_income': monthly_income,
        'weekly_income': weekly_income,
        'daily_income': daily_income,
        'monthly_salary': monthly_salary,
        'monthly_misc_expenses': monthly_misc_expenses,
        'is_superuser': is_superuser
        # 'weekly_commission': weekly_commission,
        # 'weekly_electricity': weekly_electricity,
        # 'weekly_misc_expenses': weekly_misc_expenses,
        # 'daily_commission': daily_commission,
        # 'daily_electricity': daily_electricity,
        # 'daily_misc_expenses': daily_misc_expenses,
    }
    return render(request, 'restaurant/restaurant_statistics.html', context)


# grocery statistics
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def grocery_statistics(request):
    is_superuser = request.user.is_superuser
    # get gross income
    all_grocery = Grocery.objects.all()
    total_income = sum(all_grocery.values_list('groc_daily_sales', flat=True))

    all_expenses = GroceryExpense.objects.all()
    salary_expenses = sum(all_expenses.values_list('g_salary_expenses', flat=True))
    misc_expenses = sum(all_expenses.values_list('g_misc_expenses', flat=True))
    stock_expenses = sum(all_expenses.values_list('g_stock_expenses', flat=True))
    # calculate net income
    sum_expenses = int(salary_expenses) + int(misc_expenses) + int(stock_expenses)
    net_value = int(total_income) - int(sum_expenses)
    # get latest monthly, weekly & daily income
    monthly_income = Grocery.objects.annotate(month=TruncMonth('groc_sales_date')).values('month').annotate(
        total_amount=Sum('groc_daily_sales'))
    weekly_income = Grocery.objects.annotate(week=TruncWeek('groc_sales_date')).values('week').annotate(
        total_amount=Sum('groc_daily_sales'))
    daily_income = Grocery.objects.annotate(day=TruncDay('groc_sales_date')).values('day').annotate(
        total_amount=Sum('groc_daily_sales'))
    # get latest monthly, weekly & daily expense
    monthly_salary = GroceryExpense.objects.annotate(month=TruncMonth('g_expenditure_date')).values(
        'month').annotate(
        total_expense=Sum('g_salary_expenses'))
    monthly_misc_expenses = GroceryExpense.objects.annotate(month=TruncMonth('g_expenditure_date')).values(
        'month').annotate(
        total_expense=Sum('g_misc_expenses'))
    monthly_stock_expenses = GroceryExpense.objects.annotate(month=TruncMonth('g_expenditure_date')).values(
        'month').annotate(
        total_expense=Sum('g_stock_expenses'))

    weekly_salary = GroceryExpense.objects.annotate(week=TruncWeek('g_expenditure_date')).values('week').annotate(
        total_expense=Sum('g_salary_expenses'))
    weekly_misc_expenses = GroceryExpense.objects.annotate(week=TruncWeek('g_expenditure_date')).values(
        'week').annotate(
        total_expense=Sum('g_misc_expenses'))

    daily_salary = GroceryExpense.objects.annotate(day=TruncDay('g_expenditure_date')).values('day').annotate(
        total_expense=Sum('g_salary_expenses'))
    daily_misc_expenses = GroceryExpense.objects.annotate(day=TruncDay('g_expenditure_date')).values('day').annotate(
        total_expense=Sum('g_misc_expenses'))

    context = {
        'total_income': total_income,
        'sum_expenses': sum_expenses,
        'net_value': net_value,
        'monthly_income': monthly_income,
        'weekly_income': weekly_income,
        'daily_income': daily_income,
        'monthly_salary': monthly_salary,
        'monthly_misc_expenses': monthly_misc_expenses,
        'monthly_stock_expenses': monthly_stock_expenses,
        'is_superuser': is_superuser
        # 'weekly_commission': weekly_commission,
        # 'weekly_electricity': weekly_electricity,
        # 'weekly_misc_expenses': weekly_misc_expenses,
        # 'daily_commission': daily_commission,
        # 'daily_electricity': daily_electricity,
        # 'daily_misc_expenses': daily_misc_expenses,
    }
    return render(request, 'grocery/grocery_statistics.html', context)


# view all cars (backend)
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def view_more(request):
    cars = Car.objects.all().order_by('-id')[:1]
    context = {
        'cars': cars,
    }
    return render(request, 'carwash/view_more.html', context)


# view all car wash expenses (backend)
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def view_more_expense(request):
    exps = Expenses.objects.all().order_by('-id')[:1]
    context = {
        'exps': exps
    }
    return render(request, 'carwash/view_more_expense.html', context)


# view all restaurant expenses (backend)
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def view_more_rest_expense(request):
    rest_exp = RestaurantExpense.objects.all().order_by('-id')[:1]
    context = {
        'rest_exp': rest_exp
    }
    return render(request, 'restaurant/view_more_rest_expense.html', context)


# view all grocery expenses (backend)
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def view_more_groc_expense(request):
    groc_exp = GroceryExpense.objects.all().order_by('-id')[:1]
    context = {
        'groc_exp': groc_exp
    }
    return render(request, 'grocery/view_more_groc_expense.html', context)


# view all cars
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def view_all_cars(request):
    is_superuser = request.user.is_superuser
    cars = Car.objects.all()
    cars_number = cars.count()
    # get gross income
    total_income = sum(cars.values_list('servicing_cost', flat=True))
    # get total expenses
    expenses_all = Expenses.objects.all()
    commissioning_expenses = sum(expenses_all.values_list('daily_commission', flat=True))
    electricity_expenses = sum(expenses_all.values_list('electricity', flat=True))
    misc_expenses = sum(expenses_all.values_list('misc_expenses', flat=True))
    rent_expenses = sum(expenses_all.values_list('rent', flat=True))
    # get net income
    sum_expenses = int(commissioning_expenses) + int(electricity_expenses) + int(misc_expenses) + int(rent_expenses)
    net_value = int(total_income) - int(sum_expenses)

    context = {
        'cars': cars,
        'cars_number': cars_number,
        'sum_expenses': sum_expenses,
        'net_value': net_value,
        'total_income': total_income,
        'is_superuser': is_superuser
    }
    return render(request, 'carwash/view_all_cars.html', context)


# view all restaurant
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def view_more_restaurant(request):
    rest = Restaurant.objects.all().order_by('-id')[:1]
    monthly_income = Restaurant.objects.annotate(month=TruncMonth('rest_sales_date')).values('month').annotate(
        total_amount=Sum('rest_daily_sales'))
    weekly_income = Restaurant.objects.annotate(week=TruncWeek('rest_sales_date')).values('week').annotate(
        total_amount=Sum('rest_daily_sales'))
    daily_income = Restaurant.objects.annotate(day=TruncDay('rest_sales_date')).values('day').annotate(
        total_amount=Sum('rest_daily_sales'))
    context = {
        'rest': rest,
        'monthly_income': monthly_income,
        'weekly_income': weekly_income,
        'daily_income': daily_income
    }
    return render(request, 'restaurant/view_more_restaurant.html', context)


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def view_all_restaurant(request):
    is_superuser = request.user.is_superuser
    rest = Restaurant.objects.all()
    # get gross income
    total_income = sum(rest.values_list('rest_daily_sales', flat=True))
    # get total expenses
    rest_expenses = RestaurantExpense.objects.all()
    salary_expenses = sum(rest_expenses.values_list('r_salary_expenses', flat=True))
    misc_expenses = sum(rest_expenses.values_list('r_misc_expenses', flat=True))
    # get net income
    sum_expenses = int(salary_expenses) + int(misc_expenses)
    net_value = int(total_income) - int(sum_expenses)
    context = {
        'rest': rest,
        'total_income': total_income,
        'sum_expenses': sum_expenses,
        'net_value': net_value,
        'is_superuser': is_superuser
    }
    return render(request, 'restaurant/view_all_restaurant.html', context)


# view all grocery
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def view_more_grocery(request):
    groc = Grocery.objects.all().order_by('-id')[:1]
    context = {
        'groc': groc,
    }
    return render(request, 'grocery/view_more_grocery.html', context)


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def view_all_grocery(request):
    is_superuser = request.user.is_superuser
    groc = Grocery.objects.all()
    # get gross income
    total_income = sum(groc.values_list('groc_daily_sales', flat=True))
    # get total expenses
    groc_expenses = GroceryExpense.objects.all()
    salary_expenses = sum(groc_expenses.values_list('g_salary_expenses', flat=True))
    misc_expenses = sum(groc_expenses.values_list('g_misc_expenses', flat=True))
    stock_expenses = sum(groc_expenses.values_list('g_stock_expenses', flat=True))
    # get net income
    sum_expenses = int(salary_expenses) + int(misc_expenses) + int(stock_expenses)
    net_value = int(total_income) - int(sum_expenses)
    context = {
        'groc': groc,
        'total_income': total_income,
        'sum_expenses': sum_expenses,
        'net_value': net_value,
        'is_superuser': is_superuser
    }
    return render(request, 'grocery/view_all_grocery.html', context)


# display specific car details (backend)
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def car_detail(request, id):
    try:
        car = Car.objects.get(id=id)
    except Car.DoesNotExist:
        raise Http404('Car Details Not Found!')
    context = {
        'car': car
    }
    return render(request, 'carwash/car_detail.html', context)


# car wash specific exp details (backend)
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def expense_detail(request, id):
    try:
        exp = Expenses.objects.get(id=id)
    except Expenses.DoesNotExist:
        raise Http404('Car Details Not Found!')
    context = {
        'exp': exp
    }
    return render(request, 'carwash/expense_detail.html', context)


# restaurant specific exp details (backend)
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def rest_expense_detail(request, id):
    try:
        rest_exp = RestaurantExpense.objects.get(id=id)
    except RestaurantExpense.DoesNotExist:
        raise Http404('Restaurant Details Not Found!')
    context = {
        'rest_exp': rest_exp
    }
    return render(request, 'restaurant/rest_expense_detail.html', context)


# display specific restaurant details
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def restaurant_detail(request, id):
    try:
        rest = Restaurant.objects.get(id=id)
    except Restaurant.DoesNotExist:
        raise Http404('Restaurant Details NOT FOUND!')
    context = {
        'rest': rest
    }
    return render(request, 'restaurant/restaurant_detail.html', context)


# display specific grocery details
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def grocery_detail(request, id):
    try:
        groc = Grocery.objects.get(id=id)
    except Grocery.DoesNotExist:
        raise Http404('Grocery Details NOT FOUND!')
    context = {
        'groc': groc
    }
    return render(request, 'grocery/grocery_detail.html', context)


# update car data (backend)
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def update(request, id):
    is_superuser = request.user.is_superuser
    if is_superuser:
        listing = Car.objects.get(id=id)
        form = CarForm(instance=listing)
        if request.method == 'POST':
            form = CarForm(request.POST, instance=listing)
            if form.is_valid():
                messages.success(request, 'SUCCESS! Car Updated Successfully.')
                form.save()
                return redirect('/car_wash')
            else:
                messages.error(request, 'FAILED! Something Went Wrong.')
                context = {
                    'form': form
                }
                return render(request, 'carwash/update.html', context)
        context = {
            'form': form
        }
        return render(request, 'carwash/update.html', context)
    else:
        return redirect('/car_wash')


# update restaurant data
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def update_rest_data(request, id):
    is_superuser = request.user.is_superuser
    if is_superuser:
        listing = Restaurant.objects.get(id=id)
        form = RestaurantForm(instance=listing)
        if request.method == 'POST':
            form = RestaurantForm(request.POST, instance=listing)
            if form.is_valid():
                messages.success(request, 'SUCCESS! Restaurant Updated Successfully.')
                form.save()
                return redirect('/restaurant')
            else:
                messages.error(request, 'FAILED! Something Went Wrong.')
                context = {
                    'form': form
                }
                return render(request, 'restaurant/update_rest_data.html', context)
        context = {
            'form': form
        }
        return render(request, 'restaurant/update_rest_data.html', context)
    else:
        return redirect('/restaurant')


# update grocery data
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def update_groc_data(request, id):
    is_superuser = request.user.is_superuser
    if is_superuser:
        listing = Grocery.objects.get(id=id)
        form = GroceryForm(instance=listing)
        if request.method == 'POST':
            form = GroceryForm(request.POST, instance=listing)
            if form.is_valid():
                messages.success(request, 'SUCCESS! Grocery Updated Successfully.')
                form.save()
                return redirect('/grocery')
            else:
                messages.error(request, 'FAILED! Something Went Wrong.')
                context = {
                    'form': form
                }
                return render(request, 'grocery/update_groc_data.html', context)
        context = {
            'form': form
        }
        return render(request, 'grocery/update_groc_data.html', context)
    else:
        return redirect('/grocery')


# delete car data (backend)
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete(request, id):
    is_superuser = request.user.is_superuser
    if is_superuser:
        listing = Car.objects.get(id=id)
        listing.delete()
        messages.success(request, 'Car Data Deleted Successfully!')
        return redirect('/car_wash')
    else:
        return redirect('/car_wash')


# delete restaurant data
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_rest_data(request, id):
    is_superuser = request.user.is_superuser
    if is_superuser:
        listing = Restaurant.objects.get(id=id)
        listing.delete()
        messages.success(request, 'Restaurant Data Deleted Successfully')
        return redirect('/restaurant')
    else:
        return redirect('/restaurant')


# delete grocery data
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_groc_data(request, id):
    is_superuser = request.user.is_superuser
    if is_superuser:
        listing = Grocery.objects.get(id=id)
        listing.delete()
        messages.success(request, 'Grocery Data Deleted Successfully')
        return redirect('/grocery')
    else:
        return redirect('/grocery')


# add car data (backend)
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add(request):
    form = CarForm()
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'SUCCESS! Car Added Successfully.')
            return redirect('/print_pdf')
        else:
            messages.error(request, 'FAILED! Car Did Not Add Successfully.')
            context = {
                'form': form
            }
            return render(request, 'carwash/add.html', context)
    context = {
        'form': form
    }
    return render(request, 'carwash/add.html', context)


# add car expense
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_expense(request):
    form = ExpensesForm()
    if request.method == 'POST':
        form = ExpensesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'SUCCESS! Successfully Update Expense.')
            return redirect('/car_wash')
        else:
            messages.error(request, 'FAILED!  Did not update Expense')
            context = {
                'form': form
            }
            return render(request, 'carwash/add_expense.html', context)
    context = {
        'form': form
    }
    return render(request, 'carwash/add_expense.html', context)


#  add restaurant expense
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_restaurant_expense(request):
    form = RestaurantExpenseForm()
    if request.method == 'POST':
        form = RestaurantExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'SUCCESS! Successfully Update Expense.')
            return redirect('/restaurant')
        else:
            messages.error(request, 'FAILED!  Did not update Expense')
            context = {
                'form': form
            }
            return render(request, 'restaurant/add_restaurant_expense.html', context)
    context = {
        'form': form
    }
    return render(request, 'restaurant/add_restaurant_expense.html', context)


# add grocery expense
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_grocery_expense(request):
    form = GroceryExpenseForm()
    if request.method == 'POST':
        form = GroceryExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'SUCCESS! Successfully Update Expense.')
            return redirect('/grocery')
        else:
            messages.error(request, 'FAILED!  Did not update Expense')
            context = {
                'form': form
            }
            return render(request, 'grocery/add_grocery_expense.html', context)
    context = {
        'form': form
    }
    return render(request, 'grocery/add_grocery_expense.html', context)


# print car pdf
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def print_pdf(request):
    data = Car.objects.all().order_by('-id')[:1]
    context = {
        'data': data
    }
    return render(request, 'carwash/print_pdf.html', context)


# print restaurant pdf
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def print_rest_pdf(request):
    rest_data = Restaurant.objects.all().order_by('-id')[:1]
    context = {
        'rest_data': rest_data
    }
    return render(request, 'restaurant/print_rest_pdf.html', context)


# print grocery pdf
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def print_groc_pdf(request):
    groc_data = Grocery.objects.all().order_by('-id')[:1]
    context = {
        'groc_data': groc_data
    }
    return render(request, 'grocery/print_groc_pdf.html', context)


# add restaurant data (backend)
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_rest(request):
    form = RestaurantForm()
    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'SUCCESS! Details Added Successfully.')
            return redirect('/print_rest_pdf')
        else:
            messages.error(request, 'FAILED! Details Did Not Add Successfully.')
            context = {
                'form': form
            }
            return render(request, 'restaurant/add_rest.html', context)
    context = {
        'form': form
    }
    return render(request, 'restaurant/add_rest.html', context)


# add grocery data (backend)
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_grocery(request):
    form = GroceryForm()
    if request.method == 'POST':
        form = GroceryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'SUCCESS! Details Added Successfully.')
            return redirect('/print_groc_pdf')
        else:
            messages.error(request, 'FAILED! Details Did Not Add Successfully.')
            context = {
                'form': form
            }
            return render(request, 'grocery/add_grocery.html', context)
    context = {
        'form': form
    }
    return render(request, 'grocery/add_grocery.html', context)


def service_bay(request):
    return render(request, 'backend/service_bay.html')


""" START CSV DOWNLOADS"""


# export car data to csv (backend)
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def export_csv(request):
    cars = Car.objects.all()
    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename=cars_export.csv'
    writer = csv.writer(response)
    writer.writerow(['Car Model', 'Car Number', 'Car Description', 'Car Notes', 'Car Owner Name', 'Car Owner Number',
                     'Service Type', 'Additional Service', 'Submission Date', 'Service Cost'])
    cars_fields = cars.values_list('car_model', 'car_number', 'car_description', 'car_notes', 'car_owner_name',
                                   'car_owner_number', 'service_type', 'servicing', 'submission_date', 'servicing_cost')
    for car in cars_fields:
        writer.writerow(car)
    return response


# export restaurant data to csv (backend)
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def export_csv_restaurant(request):
    rest_data = Restaurant.objects.all()
    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename=restaurant_export.csv'
    writer = csv.writer(response)
    writer.writerow(['Date', 'Restaurant Total Sales', 'Restaurant Total Expenses', 'Restaurant Net Sales'])
    rest_fields = rest_data.values_list('rest_sales_date', 'rest_daily_sales', 'rest_daily_expenses', 'rest_net_sales')

    for r_data in rest_fields:
        writer.writerow(r_data)
    return response


# export grocery data to csv (backend)
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def export_csv_grocery(request):
    groc_data = Grocery.objects.all()
    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename=grocery_export.csv'
    writer = csv.writer(response)
    writer.writerow(['Date', 'Grocery Total Sales'])
    groc_fields = groc_data.values_list('groc_sales_date', 'groc_daily_sales')

    for g_data in groc_fields:
        writer.writerow(g_data)
    return response


""" END CSV DOWNLOADS"""

""" START VIEW REPORTS"""


# view car report (backend)
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def report(request):
    is_superuser = request.user.is_superuser
    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        search_result = Car.objects.raw(
            'select id, car_model, car_number, car_description, car_notes, car_owner_name, car_owner_number, service_type, servicing, submission_date, servicing_cost from carapp_car where submission_date between "' + from_date + '" and "' + to_date + '"')
        context = {
            'carz': search_result,
            'is_superuser': is_superuser
        }
        return render(request, 'carwash/view_all_cars.html', context)
    else:
        carz = Car.objects.all()
        context = {
            'carz': carz,
            'is_superuser': is_superuser
        }
    return render(request, 'carwash/view_all_cars.html', context)


# view restaurant report (backend)
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def restaurant_report(request):
    is_superuser = request.user.is_superuser
    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        search_result = Restaurant.objects.raw(
            'select id, rest_sales_date, rest_daily_sales from carapp_restaurant where rest_sales_date between "' + from_date + '" and "' + to_date + '"')
        context = {
            'rest_data': search_result,
            'is_superuser': is_superuser
        }
        return render(request, 'restaurant/view_all_restaurant.html', context)
    else:
        rest_data = Restaurant.objects.all()
        context = {
            'rest_data': rest_data,
            'is_superuser': is_superuser
        }
        return render(request, 'restaurant/view_all_restaurant.html', context)


# view grocery report (backend)
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def grocery_report(request):
    is_superuser = request.user.is_superuser
    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        search_result = Grocery.objects.raw(
            'select id, groc_sales_date, groc_daily_sales from carapp_grocery where groc_sales_date between "' + from_date + '" and "' + to_date + '"')
        context = {
            'groc_data': search_result,
            'is_superuser': is_superuser
        }
        return render(request, 'grocery/grocery_report.html', context)
    else:
        groc_data = Grocery.objects.all()
        context = {
            'groc_data': groc_data,
            'is_superuser': is_superuser
        }
        return render(request, 'grocery/grocery_report.html', context)


""" END VIEW REPORTS """


def service_center(request):
    return render(request, 'backend/service_center.html')


# Company Report
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def all_reports(request):
    is_superuser = request.user.is_superuser
    # restaurant report
    rest_all = Restaurant.objects.all()
    rest_sales_total = sum(rest_all.values_list('rest_daily_sales', flat=True))
    # get restaurant expenses
    rest_all_expenses = RestaurantExpense.objects.all()
    rest_salary = sum(rest_all_expenses.values_list('r_salary_expenses', flat=True))
    rest_misc = sum(rest_all_expenses.values_list('r_misc_expenses', flat=True))
    # get restaurant net sales
    rest_expenses_total = int(rest_salary) + int(rest_misc)
    rest_net_total = int(rest_sales_total) - int(rest_expenses_total)

    # grocery report
    groc_all = Grocery.objects.all()
    groc_sales_total = sum(groc_all.values_list('groc_daily_sales', flat=True))
    # get grocery expenses
    groc_all_expenses = GroceryExpense.objects.all()
    groc_salary = sum(groc_all_expenses.values_list('g_salary_expenses', flat=True))
    groc_misc = sum(groc_all_expenses.values_list('g_misc_expenses', flat=True))
    groc_stock = sum(groc_all_expenses.values_list('g_stock_expenses', flat=True))
    # get grocery net sales
    groc_expenses_total = int(groc_salary) + int(groc_misc) + int(groc_stock)
    groc_net_total = int(groc_sales_total) - int(groc_expenses_total)

    # car wash report
    cars = Car.objects.all()
    cars_number = cars.count()
    cars_sales_total = sum(cars.values_list('servicing_cost', flat=True))
    # get car wash total expenses
    cars_all_expenses = Expenses.objects.all()
    daily_commission = sum(cars_all_expenses.values_list('daily_commission', flat=True))
    electricity = sum(cars_all_expenses.values_list('electricity', flat=True))
    misc_expenses = sum(cars_all_expenses.values_list('misc_expenses', flat=True))
    rent_expenses = sum(cars_all_expenses.values_list('rent', flat=True))
    # get car wash net sales
    total_expenses = int(daily_commission) + int(electricity) + int(misc_expenses) + int(rent_expenses)
    net_sales = int(cars_sales_total) - int(total_expenses)

    # company net value
    gross_income_total = int(rest_sales_total) + int(groc_sales_total) + int(cars_sales_total)
    expenses_total = int(rest_expenses_total) + int(groc_expenses_total) + int(total_expenses)
    net_income_total = int(gross_income_total) - int(expenses_total)

    context = {
        'rest_sales_total': rest_sales_total,
        'groc_sales_total': groc_sales_total,
        'rest_expenses_total': rest_expenses_total,
        'groc_expenses_total': groc_expenses_total,
        'rest_net_total': rest_net_total,
        'groc_net_total': groc_net_total,
        'cars_number': cars_number,
        'cars_sales_total': cars_sales_total,
        'total_expenses': total_expenses,
        'electricity': electricity,
        'net_sales': net_sales,
        'net_income_total': net_income_total,
        'expenses_total': expenses_total,
        'gross_income_total': gross_income_total,
        'is_superuser': is_superuser
    }
    return render(request, 'backend/all_reports.html', context)


# view restaurant data (backend)
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def restaurant(request):
    # topbar records display
    now = datetime.datetime.now()
    # get total income
    rest_data = Restaurant.objects.all()
    rest_income = sum(rest_data.values_list('rest_daily_sales', flat=True))
    # get total expenses
    rest_expense = RestaurantExpense.objects.all()
    salary_expenses = sum(rest_expense.values_list('r_salary_expenses', flat=True))
    misc_expenses = sum(rest_expense.values_list('r_misc_expenses', flat=True))
    # get net income
    sum_expenses = int(salary_expenses) + int(misc_expenses)
    total_income = int(rest_income) - int(sum_expenses)
    context = {
        'rest_data': rest_data,
        'year': now.year,
        'month': now.strftime('%B'),
        # 'total_income': total_income
    }
    return render(request, 'backend/restaurant.html', context)


# view grocery data (backend)
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def grocery(request):
    # topbar records display
    now = datetime.datetime.now()
    # get total income
    groc_data = Grocery.objects.all()
    groc_income = sum(groc_data.values_list('groc_daily_sales', flat=True))
    # get total expenses
    groc_expense = GroceryExpense.objects.all()
    salary_expenses = sum(groc_expense.values_list('g_salary_expenses', flat=True))
    misc_expenses = sum(groc_expense.values_list('g_misc_expenses', flat=True))
    stock_expenses = sum(groc_expense.values_list('g_stock_expenses', flat=True))
    # get net income
    sum_expenses = int(salary_expenses) + int(misc_expenses) + int(stock_expenses)
    total_income = int(groc_income) - int(sum_expenses)

    context = {
        'groc_data': groc_data,
        'year': now.year,
        'month': now.strftime('%B'),
        # 'total_income': total_income
    }
    return render(request, 'backend/grocery.html', context)
