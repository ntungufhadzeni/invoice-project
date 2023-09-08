from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import get_user_model
from django import forms
from .models import Company


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name',
                  'logo',
                  'billing_address',
                  'bank_name',
                  'account_number',
                  'branch_name',
                  'branch_code',
                  'branch_code_electronic',
                  'contact_number',
                  'email',
                  'currency']

    currency = forms.ChoiceField(choices=Company.CURRENCY_CHOICES)


class SignupForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name',
                  'email', 'password1', 'password2')
