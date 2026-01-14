"""
Serializers for Expense Tracker API.
Converts Django models to JSON and validates incoming data.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Expense, Profile


class UserSerializer(serializers.ModelSerializer):
    """Serialize User model for API responses."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class ProfileSerializer(serializers.ModelSerializer):
    """Serialize user profile with nested User data."""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Profile
        fields = ['id', 'user', 'bio', 'profile_pic']
        read_only_fields = ['id', 'user']


class ExpenseSerializer(serializers.ModelSerializer):
    """
    Serialize Expense model for API.
    Validates category, amount, and date fields.
    """
    user = UserSerializer(read_only=True)
    category_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Expense
        fields = ['id', 'user', 'title', 'amount', 'category', 'category_display', 'date', 'description']
        read_only_fields = ['id', 'user']
    
    def get_category_display(self, obj):
        """Return human-readable category name."""
        return obj.get_category_display()
    
    def validate_amount(self, value):
        """Ensure amount is positive."""
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0.")
        return value
    
    def create(self, validated_data):
        """Automatically set user to the requesting user."""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ExpenseListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for expense lists (less data)."""
    category_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Expense
        fields = ['id', 'title', 'amount', 'category', 'category_display', 'date']
    
    def get_category_display(self, obj):
        return obj.get_category_display()


class ExpenseDetailSerializer(ExpenseSerializer):
    """Detailed serializer with all fields for single expense view."""
    pass
