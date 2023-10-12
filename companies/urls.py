from django.urls import path
from django.contrib.auth.decorators import login_required
from companies.views import company_list, IndexView, edit_company, CreateCompanyView, remove_company

urlpatterns = [
    path('', login_required(IndexView.as_view()), name='home'),
    path('companies/', company_list, name='company_list'),
    path('companies/remove/<str:pk>/', remove_company, name='remove_company'),
    path('companies/edit/<str:pk>/', edit_company, name='edit_company'),
    path('companies/create/', CreateCompanyView.as_view(), name='create_company'),
]
