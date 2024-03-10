# Generated by Django 4.2.5 on 2024-01-06 16:31

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    replaces = [('invoices', '0001_initial'), ('invoices', '0002_alter_invoice_balance_alter_invoice_total_amount'), ('invoices', '0003_alter_invoice_invoice_number'), ('invoices', '0004_invoice_customer_phone')]

    initial = True

    dependencies = [
        ('companies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('invoice_number', models.CharField(max_length=20)),
                ('customer', models.CharField(max_length=100)),
                ('customer_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('billing_address', models.TextField(blank=True, null=True)),
                ('date', models.DateField()),
                ('due_date', models.DateField(blank=True, null=True)),
                ('message', models.TextField(default='Thank you for doing business with us.')),
                ('tax_rate', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('balance', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=9, null=True)),
                ('total_amount', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=9, null=True)),
                ('status', models.BooleanField(default=False)),
                ('type', models.CharField(choices=[('INV', 'Invoice'), ('QUO', 'Quotation')], default='INV', max_length=3)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.company')),
                ('customer_phone', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LineItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('service_description', models.TextField()),
                ('quantity', models.IntegerField()),
                ('rate', models.DecimalField(decimal_places=2, max_digits=9)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoices.invoice')),
            ],
        ),
    ]