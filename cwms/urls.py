from django.contrib import admin
from django.urls import path, include
from carapp import views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Frontend
    path('', views.frontend, name='frontend'),
    path('carwash/', views.carwash, name='carwash'),
    path('rest/', views.rest, name='rest'),
    path('groceries/', views.groceries, name='groceries'),

    # Backend
    path('backend/', views.backend, name='backend'),
    path('servicing/<id>/', views.car_detail, name='car_detail'),

    # Car Wash
    path('car_wash/', views.car_wash, name='car_wash'),
    path('add/', views.add, name='add'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('expense_detail/<id>/', views.expense_detail, name='expense_detail'),
    path('view_more/', views.view_more, name='view_more'),
    path('view_more_expense/', views.view_more_expense, name='view_more_expense'),
    path('view_all_cars', views.view_all_cars, name='view_all_cars'),
    path('carwash_statistics', views.carwash_statistics, name='carwash_statistics'),
    path('print_pdf/', views.print_pdf, name='print_pdf'),
    path('report/', views.report, name='report'),
    path('update/<id>/', views.update, name='update'),
    path('delete/<id>/', views.delete, name='delete'),
    path('export_csv/', views.export_csv, name='export_csv'),

    # Restaurant
    path('restaurant/', views.restaurant, name='restaurant'),
    path('restaurant/add_rest/', views.add_rest, name='add_rest'),
    path('restaurant/add_restaurant_expense/', views.add_restaurant_expense, name='add_restaurant_expense'),
    path('restaurant_statistics', views.restaurant_statistics, name='restaurant_statistics'),
    path('restaurant/view_more_restaurant/', views.view_more_restaurant, name='view_more_restaurant'),
    path('restaurant/view_more_rest_expense/', views.view_more_rest_expense, name='view_more_rest_expense'),
    path('restaurant/rest_expense_detail/<id>/', views.rest_expense_detail, name='rest_expense_detail'),
    path('view_all_restaurant/', views.view_all_restaurant, name='view_all_restaurant'),
    path('restaurant/restaurant_detail/<id>/', views.restaurant_detail, name='restaurant_detail'),
    path('update_rest_data/<id>/', views.update_rest_data, name='update_rest_data'),
    path('delete_rest_data/<id>/', views.delete_rest_data, name='delete_rest_data'),
    path('print_rest_pdf/', views.print_rest_pdf, name='print_rest_pdf'),
    path('restaurant_report/', views.restaurant_report, name='restaurant_report'),
    path('export_csv_restaurant/', views.export_csv_restaurant, name='export_csv_restaurant'),

    # Grocery
    path('grocery/', views.grocery, name='grocery'),
    path('grocery/add_grocery/', views.add_grocery, name='add_grocery'),
    path('grocery/add_grocery_expense/', views.add_grocery_expense, name='add_grocery_expense'),
    path('grocery/grocery_statistics', views.grocery_statistics, name='grocery_statistics'),
    path('view_more_grocery/', views.view_more_grocery, name='view_more_grocery'),
    path('view_more_groc_expense/', views.view_more_groc_expense, name='view_more_groc_expense'),
    path('grocery/view_all_grocery/', views.view_all_grocery, name='view_all_grocery'),
    path('grocery/grocery_detail/<id>/', views.grocery_detail, name='grocery_detail'),
    path('update_groc_data/<id>/', views.update_groc_data, name='update_groc_data'),
    path('delete_groc_data/<id>/', views.delete_groc_data, name='delete_groc_data'),
    path('print_groc_pdf/', views.print_groc_pdf, name='print_groc_pdf'),
    path('grocery_report/', views.grocery_report, name='grocery_report'),
    path('export_csv_grocery/', views.export_csv_grocery, name='export_csv_grocery'),

    # misc
    path('all_reports/', views.all_reports, name='all_reports'),

    # Service Bay
    path('service_bay/', views.service_bay, name='service_bay'),
    path('service_center/', views.service_center, name='service_center'),

    # Login/Logout
    path('login/', include('django.contrib.auth.urls')),
]
