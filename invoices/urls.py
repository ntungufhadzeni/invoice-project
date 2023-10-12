from django.urls import path

from .views import (create_invoice, view_invoice,
                    generate_pdf,
                    InvoiceListView, invoice_info, change_invoice_type,
                    edit_invoice, remove_invoice)

urlpatterns = [
    path('company/<str:pk>/', InvoiceListView.as_view(), name='invoice_list'),
    path('remove/<str:pk>/', remove_invoice, name='remove_invoice'),
    path('edit/<str:pk>/', edit_invoice, name='edit_invoice'),
    path('create/<str:pk>/', create_invoice, name="create_invoice"),
    path('detail/<str:pk>/', view_invoice, name='invoice_detail'),
    path('download/<str:pk>/', generate_pdf, name='invoice_download'),
    path('info/<str:pk>/', invoice_info, name='invoice_info'),
    path('change-type/', change_invoice_type, name='change_invoice_type'),
]
