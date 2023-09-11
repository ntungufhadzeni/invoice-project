import json
import os

import extcolors
import pdfkit
from colormap import rgb2hex
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from .forms import CompanyForm, SignupForm, LineItemFormSet, InvoiceForm
from .models import Company, Invoice, LineItem


def is_white_color(rgb):
    r, g, b = rgb
    # Check if the color is white (all RGB components are at their maximum)
    return r == 255 and g == 255 and b == 255


def get_color(colors):
    brightest_color = None
    max_brightness = -1

    for (r, g, b), percent in colors:
        # Calculate brightness using the formula: 0.299*R + 0.587*G + 0.114*B
        brightness = 0.299 * r + 0.587 * g + 0.114 * b

        # Exclude white color and find the brightest color
        if not is_white_color((r, g, b)) and brightness > max_brightness:
            max_brightness = brightness
            brightest_color = rgb2hex(int(r), int(g), int(b))

    return brightest_color


@method_decorator(login_required(login_url='/login'), name='dispatch')
class IndexView(TemplateView):
    template_name = 'invoices/index.html'


class UserSignupView(View):
    template_name = 'registration/signup.html'
    form_class = SignupForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        return render(request, self.template_name, {'form': form})


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class CreateCompanyView(View):
    template_name = 'invoices/company_form.html'
    form_class = CompanyForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            company = form.save(commit=False)
            company.user = request.user  # Associate the company with the currently logged-in user
            pk = company.pk
            company.save()

            company = Company.objects.get(pk=pk)
            colors, pixel_count = extcolors.extract_from_path(company.logo.path)
            company.color = get_color(colors)
            company.save()
            return HttpResponse(status=204,
                                headers={
                                    'HX-Trigger': json.dumps({
                                        "companyListChanged": None,
                                        "showMessage": f"{company.name} added."
                                    })
                                })
        return render(request, self.template_name, {'form': form})


class InvoiceListView(View):
    template_name = 'invoices/invoice_list.html'

    def get(self, request, pk=None, **kwargs):
        invoices = Invoice.objects.filter(company__id=pk)
        context = {
            "invoices": invoices,
            "pk": pk,
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
            invoices.update(status=True)
            invoices.update(balance=0.00)

        return redirect('invoice_list', pk=pk)


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
            invoice = Invoice.objects.create(customer=form.cleaned_data.get('customer'),
                                             company=company,
                                             customer_email=form.cleaned_data.get('customer_email'),
                                             billing_address=form.cleaned_data.get('billing_address'),
                                             date=form.data['date'],
                                             due_date=form.data['due_date'],
                                             message=form.cleaned_data.get('message'),
                                             tax_rate=float(form.cleaned_data.get('tax_rate')),
                                             type=form.cleaned_data.get('type'),
                                             invoice_number=form.cleaned_data.get('invoice_number')
                                             )

            if formset.is_valid():
                total = 0
                for form in formset:
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
                return redirect('invoice_list', pk=pk)
    context = {
        "title": "Invoice Generator",
        "formset": formset,
        "form": form,
        "company": company
    }
    return render(request, 'invoices/invoice_create.html', context)


def edit_invoice(request, pk):
    # Retrieve the invoice and related line items from the database
    invoice = Invoice.objects.get(pk=pk)
    line_items = LineItem.objects.filter(invoice=invoice)

    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        formset = LineItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            # Update the invoice model instance with the edited data
            invoice.invoice_number = form.cleaned_data['invoice_number']
            invoice.customer = form.cleaned_data['customer']
            invoice.customer_email = form.cleaned_data['customer_email']
            invoice.billing_address = form.cleaned_data['billing_address']
            invoice.message = form.cleaned_data['message']
            invoice.tax_rate = form.cleaned_data['tax_rate']
            invoice.type = form.cleaned_data['type']

            # Update line items for the invoice
            total = 0
            line_items.delete()
            for form in formset:
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
            return redirect('invoice_list', pk=invoice.company.pk)

    invoice_initial = {'invoice_number': invoice.invoice_number,
                       'customer': invoice.customer,
                       'customer_email': invoice.customer_email,
                       'billing_address': invoice.billing_address,
                       'message': invoice.message,
                       'tax_rate': int(invoice.tax_rate),
                       'type': invoice.type,
                       }
    line_items_initial = [{'description': item.service_description, 'quantity': item.quantity, 'rate': item.rate, }
                          for item in line_items]
    amounts = [item.rate * item.quantity for item in line_items]
    # Initialize the formset with data from the model instances
    formset = LineItemFormSet(initial=line_items_initial)
    form = InvoiceForm(initial=invoice_initial)
    context = {'title': 'Invoice Edit', 'invoice': invoice, 'form': form, 'formset': formset, 'amounts': amounts}

    return render(request, 'invoices/edit_invoice.html', context)


def view_pdf(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    line_item = invoice.lineitem_set.all()
    context = {
        "company": invoice.company,
        "invoice": invoice,
        "lineitem": line_item,

    }
    return render(request, 'invoices/pdf_template_view.html', context)


def generate_pdf(request, pk):
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

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="invoice.pdf"'

    return response


def change_status(request, pk):
    return redirect('invoice_list', pk=pk)


def view_404(request, *args, **kwargs):
    return redirect('/')


def company_list(request):
    return render(request, 'invoices/company_list.html', {
        'companies': Company.objects.filter(user=request.user),
    })


def change_invoice_type(request):
    pk = request.POST.get('pk')
    invoice = get_object_or_404(Invoice, pk=pk)
    return JsonResponse(
        status=200,
        data={
            "invoice_id": invoice.pk,
            "invoice_number": invoice.invoice_number,
            "date": invoice.date,
            "due_date": invoice.due_date,
            "type": invoice.type,
        }
    )


def invoice_info(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return JsonResponse(
        status=200,
        data={
            "invoice_id": pk,
            "invoice_number": invoice.invoice_number,
            "date": invoice.date,
            "due_date": invoice.due_date,
        }
    )


@require_POST
def remove_company(request, pk):
    company = get_object_or_404(Company, pk=pk)
    company.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "companyListChanged": None,
                "showMessage": f"{company.name} deleted."
            })
        })


def edit_company(request, pk):
    company = get_object_or_404(Company, pk=pk)
    if request.method == "POST":
        form = CompanyForm(request.POST, request.FILES)

        if form.is_valid():
            company.name = form.cleaned_data['name']
            company.logo = form.cleaned_data['logo']
            company.billing_address = form.cleaned_data['billing_address']
            company.bank_name = form.cleaned_data['bank_name']
            company.account_number = form.cleaned_data['account_number']
            company.branch_code = form.cleaned_data['branch_code']
            company.branch_code_electronic = form.cleaned_data['branch_code_electronic']
            company.contact_number = form.cleaned_data['contact_number']
            company.email = form.cleaned_data['email']
            company.currency = form.cleaned_data['currency']
            company.save()

            company = Company.objects.get(pk=pk)
            colors, pixel_count = extcolors.extract_from_path(company.logo.path)
            company.color = get_color(colors)
            company.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "companyListChanged": None,
                        "showMessage": f"{company.name} updated."
                    })
                }
            )
    else:
        form = CompanyForm(instance=company)
    return render(request, 'invoices/company_form.html', {
        'form': form,
    })
