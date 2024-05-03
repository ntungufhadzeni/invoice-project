import json

import extcolors
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView

from companies.forms import CompanyForm
from companies.models import Company
from .utils import get_color
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(TemplateView, LoginRequiredMixin):
    template_name = 'companies/index.html'


def company_list(request):
    return render(request, 'companies/company_list.html', {
        'companies': Company.objects.filter(user=request.user),
    })


class CreateCompanyView(View, LoginRequiredMixin):
    template_name = 'companies/company_form.html'
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
            brightest_color = get_color(colors)
            company.color = brightest_color
            company.save()
            return HttpResponse(status=204,
                                headers={
                                    'HX-Trigger': json.dumps({
                                        "companyListChanged": None,
                                        "showMessage": f"{company.name} added."
                                    })
                                })
        return render(request, self.template_name, {'form': form})


@login_required
def edit_company(request, pk):
    company = Company.objects.get(pk=pk)
    if request.method == "POST":
        if request.FILES:
            form = CompanyForm(request.POST, request.FILES)
        else:
            form = CompanyForm(request.POST)
            form.fields['logo'].required = False

        if form.is_valid():
            company.name = form.cleaned_data['name']
            company.billing_address = form.cleaned_data['billing_address']
            company.bank_name = form.cleaned_data['bank_name']
            company.account_number = form.cleaned_data['account_number']
            company.branch_code = form.cleaned_data['branch_code']
            company.branch_name = form.cleaned_data['branch_name']
            company.branch_code_electronic = form.cleaned_data['branch_code_electronic']
            company.contact_number = form.cleaned_data['contact_number']
            company.email = form.cleaned_data['email']
            company.currency = form.cleaned_data['currency']
            if request.FILES:
                company.logo = form.cleaned_data['logo']
            company.save()

            if request.FILES:
                company = Company.objects.get(pk=pk)
                colors, pixel_count = extcolors.extract_from_path(company.logo.path)
                brightest_color = get_color(colors)
                company.color = brightest_color
                company.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "companyListChanged": None,
                        "showMessage": f"{company.name} details updated successfully."
                    })
                }
            )
    else:
        form = CompanyForm(instance=company)
    return render(request, 'companies/company_form.html', {
        'form': form,
    })


@login_required
def remove_company(request, pk):
    company = get_object_or_404(Company, pk=pk)
    company.delete()
    return HttpResponse(
        status=204,
        headers={
            'HX-Trigger': json.dumps({
                "companyListChanged": None,
                "showMessage": f"{company.name} successfully deleted."
            })
        })
