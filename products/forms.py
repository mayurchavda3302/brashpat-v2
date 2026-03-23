import re
from django import forms
from .models import ProductInquiry


class ProductInquiryForm(forms.ModelForm):
    """Form for product inquiry / order request with validation."""

    class Meta:
        model = ProductInquiry
        fields = ['name', 'email', 'phone', 'quantity', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name',
                'id': 'inquiry-name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your@email.com',
                'id': 'inquiry-email',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+91 XXXXX XXXXX',
                'id': 'inquiry-phone',
            }),
            'quantity': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 500 pieces',
                'id': 'inquiry-quantity',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe your requirements, specifications, or any questions...',
                'id': 'inquiry-message',
            }),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise forms.ValidationError('Name must be at least 2 characters long.')
        if not re.match(r'^[a-zA-Z\s.\'-]+$', name):
            raise forms.ValidationError('Name can only contain letters, spaces, dots, hyphens, and apostrophes.')
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if not email:
            raise forms.ValidationError('Email address is required.')
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if phone:
            cleaned = re.sub(r'[\s\-\(\)]+', '', phone)
            if not re.match(r'^\+?\d{7,15}$', cleaned):
                raise forms.ValidationError('Please enter a valid phone number (7-15 digits).')
        return phone

    def clean_message(self):
        message = self.cleaned_data.get('message', '').strip()
        if message and len(message) < 10:
            raise forms.ValidationError('Message must be at least 10 characters if provided.')
        return message
