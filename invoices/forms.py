from django import forms
from django.forms import formset_factory

from .models import Invoice, LineItem


class InvoiceForm(forms.Form):
    class Meta:
        model = Invoice

    invoice_number = forms.CharField(
        label='#',
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Invoice/Quotation Number',
            'rows': 1
        })
    )
    customer = forms.CharField(
        label='Customer',
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Customer/Company Name',
            'rows': 1
        })
    )
    customer_email = forms.CharField(
        label='Customer Email',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'customer@company.com',
            'rows': 1
        })
    )
    billing_address = forms.CharField(
        label='Billing Address',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'input',
            'placeholder': '1234 Bobcat Lane St.\nProtea\n1818',
            'rows': 4
        })
    )
    message = forms.CharField(
        label='Message/Note',
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'input',
            'placeholder': 'Message/Note to customer',
            'rows': 3
        })
    )
    tax_rate = forms.DecimalField(
        label='Tax (%)',
        widget=forms.TextInput(
            attrs={
                'class': 'input',
                'placeholder': 'Value added tax (VAT) e.g. 15',
                'rows': 1
            })
    )
    type = forms.ChoiceField(choices=Invoice.TYPE_CHOICES)
    date = forms.DateField(
        label='Date',
        widget=forms.widgets.DateInput(
            attrs={
                'type': 'date',
                'placeholder': 'yyyy-mm-dd',
                'class': 'input'})
    )
    due_date = forms.DateField(
        label='Due-Date',
        widget=forms.widgets.DateInput(
            attrs={
                'type': 'date',
                'placeholder': 'yyyy-mm-dd',
                'class': 'input'})
    )


class LineItemForm(forms.Form):
    class Meta:
        model = LineItem

    description = forms.CharField(
        label='Description',
        widget=forms.TextInput(attrs={
            'class': 'form-control input',
            'placeholder': 'Enter product/service description',
            'rows': 1
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
