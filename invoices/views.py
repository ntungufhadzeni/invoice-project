import datetime
import os

import pdfkit
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.template.loader import get_template
from django.views import View

from companies.models import Company
from .forms import LineItemFormSet, InvoiceForm
from .models import Invoice, LineItem
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class InvoiceListView(View, LoginRequiredMixin):
    template_name = 'invoices/invoice_list.html'

    def get(self, request, pk=None, **kwargs):
        company = Company.objects.get(pk=pk)
        invoices = Invoice.objects.filter(company=company)
        context = {
            "invoices": invoices,
            "pk": pk,
            "company": company,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk=None, **kwargs):
        invoice_ids = request.POST.getlist("invoice_id")

        update_status_for_invoices = int(request.POST.get('status', 0))
        invoices = Invoice.objects.filter(id__in=invoice_ids)

        if update_status_for_invoices == 0:
            for invoice_id in invoice_ids:
                try:
                    invoice = Invoice.objects.get(id=invoice_id)
                    total = invoice.total_amount
                    invoice.status = False
                    invoice.balance = total
                    invoice.save()
                except Invoice.DoesNotExist:
                    # Handle the case where an invoice with the specified ID does not exist
                    pass
        else:
            invoices.update(status=True, balance=0.00)

        return redirect('invoice_list', pk=pk)


@login_required
def create_invoice(request, pk):
    formset = LineItemFormSet()
    form = InvoiceForm()
    company = Company.objects.get(pk=pk)

    if request.method == 'GET':
        formset = LineItemFormSet(request.GET or None)
        form = InvoiceForm(request.GET or None)
    elif request.method == 'POST':
        formset = LineItemFormSet(request.POST)
        form = InvoiceForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['company_id'] = pk
            invoice = Invoice.objects.create(**data)

            total = 0
            for form in formset:
                if form.is_valid():
                    description = form.cleaned_data.get('description', '')
                    quantity = form.cleaned_data.get('quantity', 0)
                    rate = form.cleaned_data.get('rate', 0)
                    if description and quantity and rate:
                        amount = float(rate) * float(quantity)

                        total += amount
                        LineItem(invoice=invoice,
                                 service_description=description,
                                 quantity=quantity,
                                 rate=rate,
                                 amount=amount).save()

            invoice.total_amount = total
            invoice.balance = total
            invoice.save()
            messages.success(request, "Invoice created successfully.")
            return redirect('invoice_list', pk=pk)
    context = {
        "page_title": "Create Invoice",
        "formset": formset,
        "form": form,
        "company": company,
        "invoice_number": ""
    }
    return render(request, 'invoices/invoice_create.html', context)


@login_required
def edit_invoice(request, pk):
    # Retrieve the invoice and related line items from the database
    invoice = Invoice.objects.get(pk=pk)
    line_items = LineItem.objects.filter(invoice=invoice)
    if request.method == 'GET':
        invoice_initial = {'invoice_number': invoice.invoice_number,
                           'customer': invoice.customer,
                           'customer_email': invoice.customer_email,
                           'customer_phone': invoice.customer_phone,
                           'billing_address': invoice.billing_address,
                           'message': invoice.message,
                           'tax_rate': int(invoice.tax_rate),
                           'type': invoice.type,
                           'date': invoice.date,
                           'due_date': invoice.due_date,
                           }
        line_items_initial = [{'description': item.service_description, 'quantity': item.quantity, 'rate': item.rate, }
                              for item in line_items]
        # Initialize the formset with data from the model instances
        formset = LineItemFormSet(initial=line_items_initial)
        form = InvoiceForm(initial=invoice_initial)
        context = {'page_title': 'Edit Invoice', 'form': form, 'formset': formset,
                   'company': invoice.company, "invoice_number": invoice.invoice_number}
        return render(request, 'invoices/invoice_create.html', context)
    elif request.method == 'POST':
        form = InvoiceForm(request.POST)
        formset = LineItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            # Update the invoice model instance with the edited data
            invoice.invoice_number = form.cleaned_data['invoice_number']
            invoice.customer = form.cleaned_data['customer']
            invoice.customer_email = form.cleaned_data['customer_email']
            invoice.customer_phone = form.cleaned_data['customer_phone']
            invoice.billing_address = form.cleaned_data['billing_address']
            invoice.message = form.cleaned_data['message']
            invoice.tax_rate = form.cleaned_data['tax_rate']
            invoice.type = form.cleaned_data['type']

            # Update line items for the invoice
            total = 0
            line_items.delete()
            for form in formset:
                if form.is_valid():
                    description = form.cleaned_data.get('description')
                    quantity = form.cleaned_data.get('quantity')
                    rate = form.cleaned_data.get('rate')
                    if description and quantity and rate:
                        amount = float(rate) * float(quantity)

                        total += amount
                        LineItem(invoice=invoice,
                                 service_description=description,
                                 quantity=quantity,
                                 rate=rate,
                                 amount=amount).save()
            invoice.total_amount = total
            invoice.balance = total
            invoice.save()

            # Redirect to a success page or invoice detail view
            # You can customize the URL where you want to redirect
            messages.success(request, 'Invoice details updated.')
            return redirect('invoice_list', pk=invoice.company.pk)
        context = {'page_title': 'Edit Invoice', 'form': form, 'formset': formset,
                   'company': invoice.company, "invoice_number": invoice.invoice_number}
        return render(request, 'invoices/invoice_create.html', context)


@login_required
def view_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    line_item = invoice.lineitem_set.all()

    context = {
        "company": invoice.company,
        "invoice": invoice,
        "lineitem": line_item,

    }
    template = get_template('invoices/pdf_template.html')
    html = template.render(context)
    options = {
        'encoding': 'UTF-8',
        'javascript-delay': '1000',  # Optional
        'enable-local-file-access': None,  # To be able to access CSS
        'page-size': 'A4',
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
    }
    css = os.path.join(settings.STATIC_ROOT, 'css', 'invoice-template.css')
    config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
    # Use False instead of output path to save pdf to a variable

    pdf = pdfkit.from_string(html, False, configuration=config, options=options, css=css)
    if invoice.type == 'INV':
        filename = f'invoice_number_{invoice.invoice_number}.pdf'
    else:
        filename = f'quotation_number_{invoice.invoice_number}.pdf'

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{filename}"'

    return response


@login_required
def download_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    line_item = invoice.lineitem_set.all()

    context = {
        "company": invoice.company,
        "invoice": invoice,
        "lineitem": line_item,

    }
    template = get_template('invoices/pdf_template.html')
    html = template.render(context)
    options = {
        'encoding': 'UTF-8',
        'javascript-delay': '1000',  # Optional
        'enable-local-file-access': None,  # To be able to access CSS
        'page-size': 'A4',
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
    }
    css = os.path.join(settings.STATIC_ROOT, 'css', 'invoice-template.css')
    config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
    # Use False instead of output path to save pdf to a variable

    pdf = pdfkit.from_string(html, False, configuration=config, options=options, css=css)
    if invoice.type == 'INV':
        filename = f'invoice_{invoice.invoice_number}.pdf'
    else:
        filename = f'quotation_{invoice.invoice_number}.pdf'

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response


@login_required
def download_delivery_note(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    line_item = invoice.lineitem_set.all()
    today = datetime.datetime.now()

    context = {
        "company": invoice.company,
        "invoice": invoice,
        "lineitem": line_item,
        "delivery_date": today.strftime("%d/%m/%Y")

    }

    template = get_template('invoices/delivery_note_pdf_template.html')
    html = template.render(context)
    options = {
        'encoding': 'UTF-8',
        'javascript-delay': '1000',  # Optional
        'enable-local-file-access': None,  # To be able to access CSS
        'page-size': 'A4',
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
    }
    css = os.path.join(settings.STATIC_ROOT, 'css', 'invoice-template.css')
    config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
    # Use False instead of output path to save pdf to a variable

    pdf = pdfkit.from_string(html, False, configuration=config, options=options, css=css)

    filename = f'delivery_note_{invoice.invoice_number}.pdf'

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response


@login_required
def remove_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    invoice.delete()
    messages.success(request, 'Item deleted successfully')
    return redirect('invoice_list', pk=invoice.company.pk)


class InvoiceNumberValidation(View):

    def post(self, request, *args, **kwargs):
        invoice_number = self.request.POST.get('invoice_number')
        company_id = self.request.POST.get('company')
        old_invoice_number = self.request.POST.get('old_invoice_number')

        if old_invoice_number != invoice_number and Invoice.objects.filter(invoice_number=invoice_number,
                                                                           company__id=company_id).exists():
            return HttpResponse("<p class='errors' id='invoiceNumberError'>The invoice/quotation number already exists</p> \
                <button type='submit' class='button is-info' id='saveBtn' hx-swap-oob='true' disabled>Save</button>")
        else:
            return HttpResponse("<p class='errors' id='invoiceNumberError'></p> \
                <button type='submit' class='button is-info' id='saveBtn' hx-swap-oob='true'>Save</button> ")
