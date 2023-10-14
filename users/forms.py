from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

class SignupForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={
            'class': 'input', 
            'placeholder': 'Your email',
            'hx-post': reverse_lazy('email_validation'),
            'hx-target': '#emailError',
            'hx-swap': 'outerHTML',
            'hx-select': '#emailError',
            'hx-select-oob': '#submitBtn',
            'hx-trigger': 'keyup[target.value.length > 3]'
        })
    )

    first_name = forms.CharField(
        label='First Name',
        min_length=3,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Your first name',
        })
    )

    last_name = forms.CharField(
        label='Last Name',
        min_length=3,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Your last name',
        })
    )

    password1 = forms.CharField(
        min_length=8, 
        widget=forms.PasswordInput(attrs={
            'class': 'input', 
            'placeholder': 'Create password',
        }), 
        label='Password'
    )

    password2 = forms.CharField(
        min_length=8, 
        widget=forms.PasswordInput(attrs={
            'class': 'input', 
            'placeholder': 'Confirm password',
        }), 
        label='Confirm password'
    )

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    
    