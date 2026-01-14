from django import forms
from .models import Expense, Profile


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'category', 'date', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition',
                'placeholder': 'e.g., Grocery Shopping',
                'required': True,
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'w-full pl-8 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0.01',
                'required': True,
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition bg-white',
                'required': True,
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition',
                'required': True,
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition',
                'placeholder': 'Add optional notes (e.g., where you shopped, what you bought)',
                'rows': 4,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add labels
        self.fields['title'].label = 'Expense Title'
        self.fields['amount'].label = 'Amount ($)'
        self.fields['category'].label = 'Category'
        self.fields['date'].label = 'Date'
        self.fields['description'].label = 'Notes (Optional)'

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
