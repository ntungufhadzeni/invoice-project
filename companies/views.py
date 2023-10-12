import json

import extcolors
from colormap import rgb2hex
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView

from companies.forms import CompanyForm
from companies.models import Company


def get_color(colors):
    brightest_color = None
    max_brightness = -1
    white_brightness = 0.299 * 255 + 0.587 * 255 + 0.114 * 255

    for (r, g, b), percent in colors:
        # Calculate brightness using the formula: 0.299*R + 0.587*G + 0.114*B
        brightness = 0.299 * r + 0.587 * g + 0.114 * b

        # Exclude white color and find the brightest color
        if not brightness == white_brightness and max_brightness < brightness:
            max_brightness = brightness
            brightest_color = rgb2hex(int(r), int(g), int(b))

    return brightest_color or '#57B223'


@method_decorator(login_required(login_url='/login'), name='dispatch')
class IndexView(TemplateView):
    template_name = 'companies/index.html'


def company_list(request):
    return render(request, 'companies/company_list.html', {
        'companies': Company.objects.filter(user=request.user),
    })


class CreateCompanyView(View):
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
            brightest_color = get_color(colors)
            company.color = brightest_color
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
    return render(request, 'companies/company_form.html', {
        'form': form,
    })


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
