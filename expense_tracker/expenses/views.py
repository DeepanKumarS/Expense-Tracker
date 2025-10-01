from datetime import datetime, timedelta
from collections import defaultdict
import calendar

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Sum
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth, TruncYear
from django.utils.timezone import now

from .models import Expense
from .forms import ExpenseForm


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'expenses/signup.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'expenses/login.html'

class CustomLogoutView(LogoutView):
    next_page = 'login'  # redirect here after logout

@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    return render(request, 'expenses/expense_list.html', {'expenses': expenses})

@login_required
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/expense_form.html', {'form': form})

@login_required
def expense_update(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expenses/expense_form.html', {'form': form})

@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list')
    return render(request, 'expenses/expense_confirm_delete.html', {'expense': expense})



@login_required
def expense_summary(request):
    filter_type = request.GET.get('filter', 'daily')
    user_expenses = Expense.objects.filter(user=request.user).order_by('date')

    grouped_expenses = []
    total_amount = user_expenses.aggregate(total=Sum('amount'))['total'] or 0

    if filter_type == 'daily':
        daily_dict = defaultdict(list)
        for e in user_expenses:
            key = e.date
            daily_dict[key].append(e)

        for i, (day, expenses) in enumerate(sorted(daily_dict.items()), 1):
            group_total = sum(exp.amount for exp in expenses)
            grouped_expenses.append({
                'serial': f"D{i}",
                'range': day.strftime('%d-%m-%Y'),
                'total': group_total,
                'expenses': expenses
            })

    elif filter_type == 'weekly':
        weekly_dict = defaultdict(list)
        for e in user_expenses:
            year, week_num, _ = e.date.isocalendar()
            key = (year, week_num)
            weekly_dict[key].append(e)

        for i, ((year, week_num), expenses) in enumerate(sorted(weekly_dict.items()), 1):
            # Calculate week start and end dates
            week_start = min(exp.date for exp in expenses)
            week_end = max(exp.date for exp in expenses)
            group_total = sum(exp.amount for exp in expenses)
            grouped_expenses.append({
                'serial': f"W{i}",
                'range': f"{week_start.strftime('%d-%m-%Y')} to {week_end.strftime('%d-%m-%Y')}",
                'total': group_total,
                'expenses': expenses
            })

    elif filter_type == 'monthly':
        monthly_dict = defaultdict(list)
        for e in user_expenses:
            key = (e.date.year, e.date.month)
            monthly_dict[key].append(e)

        for i, ((year, month), expenses) in enumerate(sorted(monthly_dict.items()), 1):
            month_start = min(exp.date for exp in expenses)
            month_end = max(exp.date for exp in expenses)
            group_total = sum(exp.amount for exp in expenses)
            month_name = calendar.month_name[month]
            grouped_expenses.append({
                'serial': f"M{i}",
                'range': f"{month_start.strftime('%d-%m-%Y')} to {month_end.strftime('%d-%m-%Y')}",
                'total': group_total,
                'expenses': expenses
            })

    elif filter_type == 'yearly':
        yearly_dict = defaultdict(list)
        for e in user_expenses:
            key = e.date.year
            yearly_dict[key].append(e)

        for i, (year, expenses) in enumerate(sorted(yearly_dict.items()), 1):
            year_start = min(exp.date for exp in expenses)
            year_end = max(exp.date for exp in expenses)
            group_total = sum(exp.amount for exp in expenses)
            grouped_expenses.append({
                'serial': f"Y{i}",
                'range': f"{year_start.strftime('%d-%m-%Y')} to {year_end.strftime('%d-%m-%Y')}",
                'total': group_total,
                'expenses': expenses
            })

    context = {
        'grouped_expenses': grouped_expenses,
        'total_amount': total_amount,
        'filter_type': filter_type,
    }

    return render(request, 'expenses/expense_summary.html', context)