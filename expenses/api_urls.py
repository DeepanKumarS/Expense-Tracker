"""
API URL routing for Expense Tracker.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import ExpenseViewSet, ProfileViewSet

# Create router and register viewsets
router = DefaultRouter()
router.register(r'expenses', ExpenseViewSet, basename='expense')
router.register(r'profiles', ProfileViewSet, basename='profile')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
]
