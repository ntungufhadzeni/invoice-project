from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import SignupForm, CompanyForm
from .models import Company


@login_required(login_url='/login')
def index(request):
    companies = Company.objects.filter(user=request.user)
    company_form = CompanyForm()
    if request.method == 'POST':
        selected_company = request.POST.get('selected_company')
        if selected_company:
            print(selected_company)
        else:
            print('no company')
    return render(request, 'core/index.html', {'companies': companies})


# signup page
def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


# logout page
def user_logout(request):
    logout(request)
    return redirect('login')


def create_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save(commit=False)
            company.user = request.user  # Associate the company with the currently logged-in user
            company.save()
            return HttpResponse(status=204)
    else:
        form = CompanyForm()
        return render(request, 'core/company_form.html', {
                'form': form,
            })  # Redirect to a page displaying a list of companies
