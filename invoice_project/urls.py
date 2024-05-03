from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('invoices/', include('invoices.urls')),
    path('', include('companies.urls')),
    path('accounts/', include('users.urls'))
]
