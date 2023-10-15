from django import forms
from django.core.validators import MinLengthValidator, RegexValidator

from companies.models import Company


class CompanyForm(forms.ModelForm):
    phone_validator = RegexValidator("^0[1-9]\d{8}$", "Invalid phone number format.")

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

    name = forms.CharField(
        label="Company Name",
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': '',
            'rows': 1
        }),
        validators=[
            MinLengthValidator(limit_value=3, message='Name must be at least 3 characters long.'),

        ]
    )
    logo = forms.ImageField(
        label="Company Logo",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    bank_name = forms.CharField(
        label="Bank Name",
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': '',
            'rows': 1
        })
    )
    account_number = forms.CharField(
        label="Account Number",
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': '',
            'rows': 1
        })
    )
    branch_name = forms.CharField(
        label="Branch Name",
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': '',
            'rows': 1
        })
    )
    branch_code = forms.CharField(
        label="Branch Code",
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': '',
            'rows': 1
        })
    )
    branch_code_electronic = forms.CharField(
        label="Branch Code (electronic)",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': '',
            'rows': 1
        })
    )
    contact_number = forms.CharField(
        label='Contact Number',
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': '0862223333',
            'rows': 1
        }),
        validators=[phone_validator]
    )
    email = forms.CharField(
        label='Email',
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'info@company.com',
            'rows': 1
        })
    )
    currency = forms.ChoiceField(choices=Company.CURRENCY_CHOICES)
    billing_address = forms.CharField(
        label='Billing address',
        widget=forms.Textarea(attrs={
            'class': 'input',
            'placeholder': '',
            'rows': 3
        })
    )
