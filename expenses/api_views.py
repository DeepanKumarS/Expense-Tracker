"""
Django REST Framework views for Expense Tracker API.
Provides CRUD operations for Expenses and Profiles.
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count
from datetime import datetime, timedelta

from .models import Expense, Profile
from .serializers import (ExpenseSerializer, ExpenseListSerializer, ExpenseDetailSerializer,
    ProfileSerializer, UserSerializer)



class ExpenseViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for Expense CRUD operations.
    
    Endpoints:
    - GET /api/expenses/ - List all user expenses (paginated)
    - POST /api/expenses/ - Create new expense
    - GET /api/expenses/{id}/ - Get expense detail
    - PUT /api/expenses/{id}/ - Update expense
    - DELETE /api/expenses/{id}/ - Delete expense
    - GET /api/expenses/stats/summary/ - Get expense summary stats
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['category', 'date']
    ordering_fields = ['date', 'amount']
    ordering = ['-date']
    search_fields = ['title', 'description']
    pagination_class = None  # Can add LimitOffsetPagination if needed
    
    def get_queryset(self):
        """Return only expenses belonging to authenticated user."""
        return Expense.objects.filter(user=self.request.user).select_related('user')
    
    def get_serializer_class(self):
        """Use appropriate serializer based on action."""
        if self.action == 'list':
            return ExpenseListSerializer
        elif self.action == 'retrieve':
            return ExpenseDetailSerializer
        return ExpenseSerializer
    
    def perform_create(self, serializer):
        """Automatically assign current user to expense."""
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        """Ensure user cannot change owner of expense."""
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def summary(self, request):
        """
        Get expense summary stats for authenticated user.
        
        Query params:
        - start_date: YYYY-MM-DD (default: 30 days ago)
        - end_date: YYYY-MM-DD (default: today)
        - category: category name (optional)
        
        Returns: total, count, by_category
        """
        # Get date range from query params
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        category = request.query_params.get('category')
        
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        else:
            start_date = datetime.now().date() - timedelta(days=30)
        
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        else:
            end_date = datetime.now().date()
        
        # Filter queryset
        qs = self.get_queryset().filter(date__range=[start_date, end_date])
        if category:
            qs = qs.filter(category=category)
        
        # Calculate stats
        total = qs.aggregate(total=Sum('amount'))['total'] or 0
        count = qs.count()
        
        # Group by category
        category_stats = []
        for cat in dict(Expense.CATEGORY_CHOICES).keys():
            cat_total = qs.filter(category=cat).aggregate(total=Sum('amount'))['total'] or 0
            cat_count = qs.filter(category=cat).count()
            if cat_count > 0:
                category_stats.append({
                    'category': cat,
                    'total': float(cat_total),
                    'count': cat_count,
                    'average': float(cat_total / cat_count) if cat_count > 0 else 0
                })
        
        return Response({
            'start_date': start_date,
            'end_date': end_date,
            'total_amount': float(total),
            'expense_count': count,
            'average_expense': float(total / count) if count > 0 else 0,
            'by_category': category_stats
        })
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def monthly_stats(self, request):
        """
        Get monthly expense breakdown for the last 12 months.
        Returns: list of {month, total, count}
        """
        from django.db.models.functions import TruncMonth
        
        twelve_months_ago = datetime.now().date() - timedelta(days=365)
        qs = self.get_queryset().filter(date__gte=twelve_months_ago)
        
        monthly_data = (
            qs.annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(total=Sum('amount'), count=Count('id'))
            .order_by('month')
        )
        
        return Response([
            {
                'month': item['month'],
                'total': float(item['total'] or 0),
                'count': item['count']
            }
            for item in monthly_data
        ])


class ProfileViewSet(viewsets.ModelViewSet):
    """
    API ViewSet for user Profile operations.
    
    Endpoints:
    - GET /api/profiles/ - List (only own profile)
    - GET /api/profiles/{id}/ - Get profile detail
    - PUT /api/profiles/{id}/ - Update own profile
    """
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return only authenticated user's profile."""
        return Profile.objects.filter(user=self.request.user).select_related('user')
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current user's profile."""
        profile = request.user.profile
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """Allow user to change their password via API."""
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if not user.check_password(old_password):
            return Response({'detail': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
        if not new_password or len(new_password) < 8:
            return Response({'detail': 'New password must be at least 8 characters.'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return Response({'detail': 'Password changed successfully.'}, status=status.HTTP_200_OK)
