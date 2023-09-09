from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import get_user_model
from django import forms
from django.forms import formset_factory

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


class InvoiceForm(forms.Form):
    # fields = ['customer', 'message']
    customer = forms.CharField(
        label='Cusomter',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Customer/Company Name',
            'rows': 1
        })
    )
    customer_email = forms.CharField(
        label='Customer Email',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'customer@company.com',
            'rows': 1
        })
    )
    billing_address = forms.CharField(
        label='Billing Address',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '',
            'rows': 1
        })
    )
    message = forms.CharField(
        label='Message/Note',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'message',
            'rows': 1
        })
    )


class LineItemForm(forms.Form):
    service = forms.CharField(
        label='Service/Product',
        widget=forms.TextInput(attrs={
            'class': 'form-control input',
            'placeholder': 'Service Name'
        })
    )
    description = forms.CharField(
        label='Description',
        widget=forms.TextInput(attrs={
            'class': 'form-control input',
            'placeholder': 'Enter Book Name here',
            "rows": 1
        })
    )
    quantity = forms.IntegerField(
        label='Qty',
        widget=forms.TextInput(attrs={
            'class': 'form-control input quantity',
            'placeholder': 'Quantity'
        })  # quantity should not be less than one
    )
    rate = forms.DecimalField(
        label='Rate $',
        widget=forms.TextInput(attrs={
            'class': 'form-control input rate',
            'placeholder': 'Rate'
        })
    )
    # amount = forms.DecimalField(
    #     disabled = True,
    #     label='Amount $',
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control input',
    #     })
    # )


LineItemFormset = formset_factory(LineItemForm, extra=1)
