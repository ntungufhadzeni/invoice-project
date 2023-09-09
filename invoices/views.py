import extcolors
import pandas as pd
import pdfkit
from colormap import rgb2hex
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView

from .forms import CompanyForm, SignupForm, LineItemFormset, InvoiceForm
from .models import Company, Invoice, LineItem


def get_color(colors):
    df_color_up = [rgb2hex(int(r), int(g), int(b)) for (r, g, b), percent in colors]
    df_percent = [percent for (_, _, _), percent in colors]

    df = pd.DataFrame(zip(df_color_up, df_percent), columns=['c_code', 'occurrence'])
    df_filtered = df[~df.c_code.isin(['#000000', '#FFFFFF'])]

    if not df_filtered.empty:
        return df_filtered['c_code'].iloc[0]
    else:
        return None


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
            return HttpResponse(status=204)
        return render(request, self.template_name, {'form': form})


class InvoiceListView(View):
    def get(self, *args, **kwargs):
        invoices = Invoice.objects.all()
        context = {
            "invoices": invoices,
        }

        return render(self.request, 'invoices/invoice_list.html', context)

    def post(self, request):
        # import pdb;pdb.set_trace()
        invoice_ids = request.POST.getlist("invoice_id")
        invoice_ids = list(map(int, invoice_ids))

        update_status_for_invoices = int(request.POST['status'])
        invoices = Invoice.objects.filter(id__in=invoice_ids)
        # import pdb;pdb.set_trace()
        if update_status_for_invoices == 0:
            invoices.update(status=False)
        else:
            invoices.update(status=True)

        return redirect('/')


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
            invoice = Invoice.objects.create(customer=form.data["customer"],
                                             customer_email=form.data["customer_email"],
                                             billing_address=form.data["billing_address"],
                                             date=form.data["date"],
                                             due_date=form.data["due_date"],
                                             message=form.data["message"],
                                             )
            # invoice.save()

            if formset.is_valid():
                # import pdb;pdb.set_trace()
                # extract name and other data from each form and save
                total = 0
                for form in formset:
                    service = form.cleaned_data.get('service')
                    description = form.cleaned_data.get('description')
                    quantity = form.cleaned_data.get('quantity')
                    rate = form.cleaned_data.get('rate')
                    if service and description and quantity and rate:
                        amount = float(rate) * float(quantity)
                        total += amount
                        LineItem(invoice=invoice,
                                 service=service,
                                 description=description,
                                 quantity=quantity,
                                 rate=rate,
                                 amount=amount).save()
                invoice.total_amount = total
                invoice.save()
                try:
                    generate_pdf(request, pk=invoice.pk)
                except Exception as e:
                    print(f"********{e}********")
                return redirect('/')
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
        "company": {
            "name": "Ibrahim Services",
            "address": "67542 Jeru, Chatsworth, CA 92145, US",
            "phone": "(818) XXX XXXX",
            "email": "contact@ibrahimservice.com",
        },
        "invoice_id": invoice.id,
        "invoice_total": invoice.total_amount,
        "customer": invoice.customer,
        "customer_email": invoice.customer_email,
        "date": invoice.date,
        "due_date": invoice.due_date,
        "billing_address": invoice.billing_address,
        "message": invoice.message,
        "lineitem": line_item,

    }
    return render(request, 'invoices/pdf_template.html', context)


def generate_pdf(request, pk):
    # Use False instead of output path to save pdf to a variable
    pdf = pdfkit.from_url(request.build_absolute_uri(reverse('invoice_detail', args=[pk])), False)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    return response


def change_status(request):
    return redirect('invoice_list')


def view_404(request, *args, **kwargs):
    return redirect('invoice_list')


def company_list(request):
    return render(request, 'invoices/company_list.html', {
        'companies': Company.objects.filter(user=request.user),
    })
