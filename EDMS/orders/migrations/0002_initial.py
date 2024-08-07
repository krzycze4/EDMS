# Generated by Django 4.2.11 on 2024-07-16 14:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("companies", "0002_alter_address_city_alter_address_country_and_more"),
        ("invoices", "0001_initial"),
        ("orders", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("contracts", "0002_contract_employee_alter_contract_company_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="protocol",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="protocols",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="company",
            field=models.ForeignKey(
                blank=True,
                help_text="The company to which the service is provided.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="orders",
                to="companies.company",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="contract",
            field=models.ForeignKey(
                help_text="The contract to which the order is attached.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="orders",
                to="contracts.contract",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="cost_invoice",
            field=models.ManyToManyField(
                blank=True,
                help_text="Cost invoices linked with the order.",
                related_name="order_from_cost_invoice",
                to="invoices.invoice",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="income_invoice",
            field=models.ManyToManyField(
                blank=True,
                help_text="Income invoices linked with the order.",
                related_name="order_from_income_invoice",
                to="invoices.invoice",
            ),
        ),
        migrations.AddField(
            model_name="order",
            name="user",
            field=models.ForeignKey(
                help_text="Employee who created the order.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
