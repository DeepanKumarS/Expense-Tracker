from django.urls import path
from . import views

urlpatterns = [
    # Expense CRUD
    path('', views.expense_list, name='expense_list'),
    path('expense/add/', views.expense_create, name='expense_create'),
    path('expense/<int:pk>/edit/', views.expense_update, name='expense_update'),
    path('expense/<int:pk>/delete/', views.expense_delete, name='expense_delete'),
    path('summary/', views.expense_summary, name='expense_summary'),
]
