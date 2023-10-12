from django.urls import path

from companies.views import company_list, IndexView, edit_company, CreateCompanyView, remove_company

urlpatterns = [
    path('', IndexView.as_view(), name='home'),
    path('companies/', company_list, name='company_list'),
    path('remove/<str:pk>/', remove_company, name='remove_company'),
    path('edit/<str:pk>/', edit_company, name='edit_company'),
    path('create/', CreateCompanyView.as_view(), name='create_company'),
]
