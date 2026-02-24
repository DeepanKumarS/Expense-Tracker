from django.contrib import admin
from .models import Expense, Profile

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'amount', 'category', 'date')
    list_filter = ('category', 'date')
    search_fields = ('title', 'user__username', 'category')
    date_hierarchy = 'date'
    ordering = ('-date',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username', 'bio')


# Optionally, unregister the default User admin and re-register with customizations if needed.
