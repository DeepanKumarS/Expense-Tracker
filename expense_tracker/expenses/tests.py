# expenses/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal
from .models import Expense
from .forms import ExpenseForm

class ExpenseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.expense = Expense.objects.create(
            user=self.user,
            title="Groceries",
            amount=Decimal("100.50"),
            category="Food",
            date="2025-09-30",
            description="Weekly groceries"
        )

    def test_expense_creation(self):
        self.assertEqual(self.expense.title, "Groceries")
        self.assertEqual(self.expense.amount, Decimal("100.50"))
        self.assertEqual(self.expense.user.username, "testuser")

    def test_str_representation(self):
        self.assertIn("Groceries", str(self.expense))
        self.assertIn("100.50", str(self.expense))


class ExpenseFormTest(TestCase):
    def test_valid_form(self):
        data = {
            "title": "Bus Ticket",
            "amount": "50.00",
            "category": "Travel",
            "date": "2025-09-30",
            "description": "Metro ride"
        }
        form = ExpenseForm(data=data)
        self.assertTrue(form.is_valid(), msg=f"Form errors: {form.errors}")

    def test_invalid_amount(self):
        data = {
            "title": "Wrong",
            "amount": "-10.00",
            "category": "Other",
            "date": "2025-09-30",
        }
        form = ExpenseForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("amount", form.errors)


class ExpenseViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="viewuser", password="viewpass")
        # Create one expense owned by user
        Expense.objects.create(
            user=self.user,
            title="Coffee",
            amount=Decimal("20.00"),
            category="Food",
            date="2025-09-30"
        )

    def test_expense_list_requires_login(self):
        # not logged in -> should redirect to login
        response = self.client.get(reverse("expense_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_expense_list_shows_user_expenses(self):
        self.client.login(username="viewuser", password="viewpass")
        response = self.client.get(reverse("expense_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Coffee")

    def test_expense_create_view(self):
        self.client.login(username="viewuser", password="viewpass")
        post_data = {
            "title": "Lunch",
            "amount": "150.00",
            "category": "Food",
            "date": "2025-09-30",
            "description": "Team lunch"
        }
        response = self.client.post(reverse("expense_create"), data=post_data)
        # after success the view redirects to expense_list (HTTP 302)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Expense.objects.filter(user=self.user).count(), 2)


# run all tests
# python manage.py test

# # run tests only for expenses app (faster)
# python manage.py test expenses

# # run a single test class or method (very useful for debugging)
# python manage.py test expenses.tests.ExpenseViewsTest.test_expense_create_view

# # increase verbosity if you want more output
# python manage.py test -v 2
