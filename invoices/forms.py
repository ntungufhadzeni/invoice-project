from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import get_user_model
from django import forms
from django.forms import formset_factory

from .models import Company, Invoice


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
    billing_address = forms.CharField(
        label='Billing address',
        widget=forms.Textarea(attrs={
            'placeholder': '',
            'rows': 3
        })
    )


class SignupForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name',
                  'email', 'password1', 'password2')


class InvoiceForm(forms.Form):
    invoice_number = forms.CharField(
        label='#',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Invoice/Quotation Number',
            'rows': 1
        })
    )
    customer = forms.CharField(
        label='Customer',
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
            'placeholder': '1234 Bobcat Lane St. Protea',
            'rows': 1
        })
    )
    message = forms.CharField(
        label='Message/Note',
        widget=forms.Textarea(attrs={
            'placeholder': '',
            'rows': 3
        })
    )
    tax_rate = forms.DecimalField(
        label='Tax (%)',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Value added tax (VAT) e.g. 15',
            'rows': 1
        })
    )
    type = forms.ChoiceField(choices=Invoice.TYPE_CHOICES)


class LineItemForm(forms.Form):
    description = forms.CharField(
        label='Description',
        widget=forms.TextInput(attrs={
            'class': 'form-control input',
            'placeholder': 'Enter product/service description',
            "rows": 1
        })
    )
    quantity = forms.IntegerField(
        label='Qty',
        widget=forms.TextInput(attrs={
            'class': 'form-control input quantity',
            'placeholder': 'Quantity e.g. 32'
        })  # quantity should not be less than one
    )
    rate = forms.DecimalField(
        label='Unit Price',
        widget=forms.TextInput(attrs={
            'class': 'form-control input rate',
            'placeholder': 'Unit Price e.g. 299.99'
        })
    )


LineItemFormSet = formset_factory(LineItemForm, extra=1)
