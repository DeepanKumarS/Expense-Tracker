import re
from datetime import date, timedelta
from django.db.models import Sum
from .models import Expense

def process_chat_query(user, query: str):
    query = query.lower()

    today = date.today()
    expenses = Expense.objects.filter(user=user)
    
    # Date filters
    if "today" in query:
        expenses = expenses.filter(date=today)
    elif "yesterday" in query:
        expenses = expenses.filter(date=today - timedelta(days=1))
    elif "this month" in query:
        expenses = expenses.filter(date__month=today.month, date__year=today.year)
    elif "last month" in query:
        prev_month = today.month - 1 or 12
        prev_year = today.year if today.month > 1 else today.year - 1
        expenses = expenses.filter(date__month=prev_month, date__year=prev_year)

    # Category filters
    category_match = re.search(r"(food|travel|entertainment|utilities|sharing|other)", query)
    if category_match:
        cat = category_match.group(1).capitalize()
        expenses = expenses.filter(category=cat)

    # Intent detection
    if "total" in query or "how much" in query:
        total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        return f"Total expenses: ₹{total:.2f}"
    elif "trend" in query:
        monthly = (Expense.objects.filter(user=user)
                    .values('date__month')
                    .annotate(total=Sum('amount'))
                    .order_by('date__month'))
        trend_text = " → ".join([f"{m['date__month']}: ₹{m['total']}" for m in monthly])
        return f"Monthly Trend: {trend_text}"
    elif "category" in query or "categories" in query:
        by_cat = (expenses.values('category')
                    .annotate(total=Sum('amount'))
                    .order_by('-total'))
        lines = [f"{x['category']}: ₹{x['total']}" for x in by_cat]
        return "\n".join(lines)
    else:
        # Default fallback
        return "I can help with queries like 'Show food expenses this month' or 'Total travel expenses today'."

