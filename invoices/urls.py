from django.urls import path
from django.contrib.auth import views as auth_views
from .views import IndexView, UserLogoutView, UserSignupView, CreateCompanyView, create_invoice, view_pdf, generate_pdf, \
    company_list, remove_company, edit_company, InvoiceListView

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('companies/', company_list, name='company_list'),
    path('invoices/<str:pk>/', InvoiceListView.as_view(), name='invoice_list'),
    path('companies/<str:pk>/remove', remove_company, name='remove_company'),
    path('companies/<str:pk>/edit', edit_company, name='edit_company'),
    path('companies/create/', CreateCompanyView.as_view(), name='create_company'),
    path('invoices/create/<str:pk>', create_invoice, name="create_invoice"),
    path('invoices/detail/<str:pk>', view_pdf, name='invoice_detail'),
    path('invoices/download/<str:pk>', generate_pdf, name='invoice_download')
]
