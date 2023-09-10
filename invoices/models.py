import os
import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from invoices.managers import UserManager


def path_and_rename(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.pk, ext)
    return os.path.join('company_logos', filename)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % self.pk


class Company(models.Model):
    CURRENCY_CHOICES = (
        ('ZAR', 'South African Rand'),
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        # Add other currency choices as needed
    )

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to=path_and_rename)
    color = models.CharField(blank=True, null=True)
    billing_address = models.TextField()
    bank_name = models.CharField(max_length=30)
    account_number = models.CharField(max_length=20)
    branch_name = models.CharField(max_length=30)
    branch_code = models.CharField(max_length=10)
    branch_code_electronic = models.CharField(max_length=10, blank=True, null=True, verbose_name="Branch code ("
                                                                                                 "electronic)")
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='ZAR')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "companies"


class Invoice(models.Model):
    TYPE_CHOICES = (
        ('INV', 'Invoice'),
        ('QUO', 'Quotation'),
    )

    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=20, unique=True)
    customer = models.CharField(max_length=100)
    customer_email = models.EmailField(null=True, blank=True)
    billing_address = models.TextField(null=True, blank=True)
    date = models.DateField()
    due_date = models.DateField(null=True, blank=True)
    message = models.TextField(default="this is a default message.")
    tax_rate = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    tax_amount = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    sub_total_amount = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    status = models.BooleanField(default=False)
    type = models.CharField(max_length=3, choices=TYPE_CHOICES, default='INV')

    def __str__(self):
        return str(self.customer)

    def get_status(self):
        return self.status


class LineItem(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    service_description = models.TextField()
    quantity = models.IntegerField()
    rate = models.DecimalField(max_digits=9, decimal_places=2)
    amount = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return str(self.invoice)
