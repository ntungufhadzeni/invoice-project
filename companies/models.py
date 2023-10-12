import os
import uuid

from django.conf import settings
from django.db import models


def path_and_rename(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.pk, ext)
    return os.path.join('company_logos', filename)


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
    color = models.CharField(max_length=25, blank=True, null=True)
    billing_address = models.TextField()
    bank_name = models.CharField(max_length=30)
    account_number = models.CharField(max_length=20)
    branch_name = models.CharField(max_length=30)
    branch_code = models.CharField(max_length=10)
    branch_code_electronic = models.CharField(max_length=10, blank=True, null=True)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='ZAR')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "companies"
