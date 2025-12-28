from django import forms
from .models import Expense, Profile


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'category', 'date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    # Custom validation for amount
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is None or amount <= 0:
            raise forms.ValidationError("Amount must be greater than 0.")
        return amount


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'w-full border rounded px-3 py-2', 'placeholder': 'Tell others about yourself...'}),
            'profile_pic': forms.ClearableFileInput(attrs={'class': 'mt-2'}),
        }
