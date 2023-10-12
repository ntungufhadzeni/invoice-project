from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('invoices/', include('invoices.urls')),
    path('companies/', include('companies.urls')),
    path('', include('users.urls'))
]
