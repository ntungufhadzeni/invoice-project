import json

import extcolors
import pdfkit
from colormap import rgb2hex
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from .forms import CompanyForm, SignupForm, LineItemFormset, InvoiceForm
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
            invoices.update(status=False)
        else:
            invoices.update(status=True)

        return redirect('invoice_list', pk=pk)


def create_invoice(request, pk):
    """
    Invoice Generator page it will have Functionality to create new invoices, 
    this will be protected view, only admin has the authority to read and make
    changes here.
    """
    formset = LineItemFormset()
    form = InvoiceForm()
    company = Company.objects.get(pk=pk)

    heading_message = 'Formset Demo'
    if request.method == 'GET':
        formset = LineItemFormset(request.GET or None)
        form = InvoiceForm(request.GET or None)
    elif request.method == 'POST':
        formset = LineItemFormset(request.POST)
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
            # invoice.save()

            if formset.is_valid():
                # import pdb;pdb.set_trace()
                # extract name and other data from each form and save
                total = 0
                total_tax = 0
                for form in formset:
                    description = form.cleaned_data.get('description')
                    quantity = form.cleaned_data.get('quantity')
                    rate = form.cleaned_data.get('rate')
                    if description and quantity and rate:
                        amount = float(rate) * float(quantity)
                        tax_amount = invoice.tax_rate / 100 * amount

                        total += amount
                        total_tax += tax_amount
                        LineItem(invoice=invoice,
                                 service_description=description,
                                 quantity=quantity,
                                 rate=rate,
                                 amount=amount).save()
                invoice.tax_amount = total_tax
                invoice.sub_total_amount = total
                invoice.total_amount = total_tax + total
                invoice.save()
                try:
                    generate_pdf(request, pk=invoice.pk)
                except Exception as e:
                    print(f"********{e}********")
                return redirect('invoice_list', pk=pk)
    context = {
        "title": "Invoice Generator",
        "formset": formset,
        "form": form,
        "company": company
    }
    return render(request, 'invoices/invoice_create.html', context)


def view_pdf(request, pk=None):
    invoice = get_object_or_404(Invoice, pk=pk)
    line_item = invoice.lineitem_set.all()

    context = {
        "company": invoice.company,
        "invoice": invoice,
        "lineitem": line_item,

    }
    return render(request, 'invoices/pdf_template.html', context)


def generate_pdf(request, pk):
    # Use False instead of output path to save pdf to a variable
    pdf = pdfkit.from_url(request.build_absolute_uri(reverse('invoice_detail', args=[pk])), False)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    return response


def change_status(request, pk):
    return redirect('invoice_list', pk=pk)


def view_404(request, *args, **kwargs):
    return redirect('/')


def company_list(request):
    return render(request, 'invoices/company_list.html', {
        'companies': Company.objects.filter(user=request.user),
    })


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
        form = CompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
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
