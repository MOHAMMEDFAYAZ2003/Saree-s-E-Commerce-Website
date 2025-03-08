from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class SignUpForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True, 
        widget=forms.TextInput(attrs={
            'placeholder': 'First and Last Name',
            'class': 'input-field'  
        })
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your Gmail',
            'class': 'input-field'
        })
    )
    
    password = forms.CharField(
        required=True,
        min_length=6,  
        widget=forms.PasswordInput(attrs={
            'placeholder': 'At least 6 Characters',
            'class': 'input-field'
        })
    )
    
    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm password',
            'class': 'input-field'
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already exists...')
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match")
        return cleaned_data

class SignInForm(forms.Form):
    email_or_username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder':'Email or Username',
            'class':'input-field'
        })
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'input-field'})
    )

