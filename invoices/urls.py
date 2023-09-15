from django.urls import path

from .views import (IndexView, UserSignupView, CreateCompanyView, create_invoice, view_invoice,
                    generate_pdf,
                    company_list, remove_company, edit_company, InvoiceListView, invoice_info, change_invoice_type,
                    edit_invoice, remove_invoice)

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('companies/', company_list, name='company_list'),
    path('invoices/<str:pk>/', InvoiceListView.as_view(), name='invoice_list'),
    path('companies/remove/<str:pk>/', remove_company, name='remove_company'),
    path('invoices/remove/<str:pk>/', remove_invoice, name='remove_invoice'),
    path('companies/edit/<str:pk>/', edit_company, name='edit_company'),
    path('invoices/edit/<str:pk>/', edit_invoice, name='edit_invoice'),
    path('companies/create/', CreateCompanyView.as_view(), name='create_company'),
    path('invoices/create/<str:pk>/', create_invoice, name="create_invoice"),
    path('invoices/detail/<str:pk>/', view_invoice, name='invoice_detail'),
    path('invoices/download/<str:pk>/', generate_pdf, name='invoice_download'),
    path('invoices/info/<str:pk>/', invoice_info, name='invoice_info'),
    path('invoices/change-type/', change_invoice_type, name='change_invoice_type'),
]
