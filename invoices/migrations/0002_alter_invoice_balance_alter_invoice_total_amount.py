# Generated by Django 4.2.5 on 2023-10-14 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='balance',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='total_amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=9, null=True),
        ),
    ]