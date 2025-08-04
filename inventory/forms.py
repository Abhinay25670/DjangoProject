from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Medicine
from datetime import date

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')
    first_name = forms.CharField(max_length=30, required=True, help_text='Required. Enter your first name.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required. Enter your last name.')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email address is already registered.')
        return email

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'batch_number', 'manufacturer', 'manufacturing_date', 
                 'expiry_date', 'quantity', 'price_per_unit', 'low_stock_threshold', 'description']
        widgets = {
            'manufacturing_date': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        manufacturing_date = cleaned_data.get('manufacturing_date')
        expiry_date = cleaned_data.get('expiry_date')
        
        if manufacturing_date and expiry_date:
            if manufacturing_date >= expiry_date:
                raise forms.ValidationError("Expiry date must be after manufacturing date.")
            
            if manufacturing_date > date.today():
                raise forms.ValidationError("Manufacturing date cannot be in the future.")
        
        return cleaned_data

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than 0.")
        return quantity

    def clean_low_stock_threshold(self):
        threshold = self.cleaned_data.get('low_stock_threshold')
        if threshold < 0:
            raise forms.ValidationError("Low stock threshold cannot be negative.")
        return threshold 