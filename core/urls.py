from django.urls import path
from django.contrib.auth import views as auth_views
from .views import IndexView, UserLogoutView, UserSignupView, CreateCompanyView, create_invoice, view_pdf, generate_pdf, \
    company_list

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('companies/', company_list, name='company_list'),
    path('create-company/', CreateCompanyView.as_view(), name='create_company'),
    path('create-invoice/<pk>', create_invoice, name="create_invoice"),
    path('invoice-detail/<pk>', view_pdf, name='invoice_detail'),
    path('invoice-download/<pk>', generate_pdf, name='invoice_download')
]
