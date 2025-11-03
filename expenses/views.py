from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Sum
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth, TruncYear
from .models import Expense
from .forms import ExpenseForm
from .chatbot_utils import process_chat_query
import calendar
from django.db import IntegrityError, transaction
from .ai_utils import predict_category

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try: 
                with transaction.atomic(): 
                    form.save()
            except IntegrityError: 
                form.add_error(None, "An account with that username already exists. Please choose another.")
            else:
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
    form = ExpenseForm()
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            if not expense.category or expense.category == 'Other':
                predicted = predict_category((expense.title or '') + ' ' + (expense.description or ''))
                        # give user a small message for debugging/feedback
                if predicted:
                    # apply predicted category
                    expense.category = predicted
                    messages.info(request, f"Predicted category: {predicted}")
            expense.save()
            return redirect('expense_list')
    return render(request, 'expenses/expense_form.html', {'form': form})

@login_required
def expense_update(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            expense = form.save(commit=False)
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
def chatbot_view(request):
    if request.method == "POST":
        user_query = request.POST.get("query")
        response = process_chat_query(request.user, user_query)
        return JsonResponse({"response": response})
    return render(request, "expenses/chatbot.html")


@login_required
def expense_summary(request):
    filter_type = request.GET.get('filter', 'daily')
    grouped_expenses = []
    total_amount = Expense.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0

    if filter_type == 'daily':
        qs = (
            Expense.objects.filter(user=request.user)
            .annotate(day=TruncDay('date'))
            .values('day')
            .annotate(total=Sum('amount'))
            .order_by('day')
        )
        for i, group in enumerate(qs, 1):
            expenses = Expense.objects.filter(user=request.user, date=group['day'])
            grouped_expenses.append({
                'serial': f"D{i}",
                'range': group['day'].strftime('%d-%m-%Y'),
                'total': group['total'],
                'expenses': expenses
            })

    elif filter_type == 'weekly':
        qs = (
            Expense.objects.filter(user=request.user)
            .annotate(week=TruncWeek('date'))
            .values('week')
            .annotate(total=Sum('amount'))
            .order_by('week')
        )
        for i, group in enumerate(qs, 1):
            week_start = group['week']
            week_end = week_start + timedelta(days=6)
            expenses = Expense.objects.filter(user=request.user, date__gte=week_start, date__lte=week_end)
            grouped_expenses.append({
                'serial': f"W{i}",
                'range': f"{week_start.strftime('%d-%m-%Y')} to {week_end.strftime('%d-%m-%Y')}",
                'total': group['total'],
                'expenses': expenses
            })

    elif filter_type == 'monthly':
        qs = (
            Expense.objects.filter(user=request.user)
            .annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(total=Sum('amount'))
            .order_by('month')
        )
        for i, group in enumerate(qs, 1):
            month_start = group['month']
            last_day = calendar.monthrange(month_start.year, month_start.month)[1]
            month_end = month_start.replace(day=last_day)
            expenses = Expense.objects.filter(user=request.user, date__year=month_start.year, date__month=month_start.month)
            month_name = calendar.month_name[month_start.month]
            grouped_expenses.append({
                'serial': f"M{i}",
                'range': f"{month_start.strftime('%d-%m-%Y')} to {month_end.strftime('%d-%m-%Y')}",
                'total': group['total'],
                'expenses': expenses
            })

    elif filter_type == 'yearly':
        qs = (
            Expense.objects.filter(user=request.user)
            .annotate(year=TruncYear('date'))
            .values('year')
            .annotate(total=Sum('amount'))
            .order_by('year')
        )
        for i, group in enumerate(qs, 1):
            year_start = group['year']
            year_end = year_start.replace(month=12, day=31)
            expenses = Expense.objects.filter(user=request.user, date__year=year_start.year)
            grouped_expenses.append({
                'serial': f"Y{i}",
                'range': f"{year_start.strftime('%d-%m-%Y')} to {year_end.strftime('%d-%m-%Y')}",
                'total': group['total'],
                'expenses': expenses
            })

    context = {
        'grouped_expenses': grouped_expenses,
        'total_amount': total_amount,
        'filter_type': filter_type,
    }

    return render(request, 'expenses/expense_summary.html', context)