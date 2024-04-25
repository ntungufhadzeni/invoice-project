from django.urls import path

from .views import (InvoiceNumberValidation, create_invoice, view_invoice,
                    download_invoice,
                    InvoiceListView,
                    edit_invoice,
                    remove_invoice,
                    download_delivery_note
                    )

urlpatterns = [
    path('company/<str:pk>/', InvoiceListView.as_view(), name='invoice_list'),
    path('remove/<str:pk>/', remove_invoice, name='remove_invoice'),
    path('edit/<str:pk>/', edit_invoice, name='edit_invoice'),
    path('create/<str:pk>/', create_invoice, name="create_invoice"),
    path('view/<str:pk>/', view_invoice, name='invoice_detail'),
    path('download/<str:pk>/', download_invoice, name='invoice_download'),
    path('download-delivery-note/<str:pk>/', download_delivery_note, name='download_delivery_note'),
    path('invoice-number-validation/', InvoiceNumberValidation.as_view(), name='invoice_number_validation')
]
