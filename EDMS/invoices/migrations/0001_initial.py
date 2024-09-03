# Generated by Django 4.2.14 on 2024-08-30 19:12

from decimal import Decimal

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("companies", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Invoice",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(help_text="Invoice name, e.g. PLAY-01-01-2024", max_length=50, unique=True)),
                (
                    "net_price",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Net value",
                        max_digits=10,
                        validators=[django.core.validators.MinValueValidator(Decimal("0.00"))],
                    ),
                ),
                (
                    "vat",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Vat value",
                        max_digits=10,
                        validators=[django.core.validators.MinValueValidator(Decimal("0.00"))],
                    ),
                ),
                (
                    "gross",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Gross value",
                        max_digits=10,
                        validators=[django.core.validators.MinValueValidator(Decimal("0.00"))],
                    ),
                ),
                ("create_date", models.DateField(help_text="Creation date")),
                ("service_date", models.DateField(help_text="Service date")),
                ("payment_date", models.DateField(help_text="Payment date")),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("original", "original"),
                            ("duplicate", "duplicate"),
                            ("proforma", "proforma"),
                            ("correcting", "correcting"),
                        ],
                        default="original",
                        help_text="Invoice type, one of original, duplicate, proforma, correcting.",
                        max_length=10,
                    ),
                ),
                ("scan", models.FileField(help_text="Physical version of the document.", upload_to="invoices/")),
                (
                    "is_paid",
                    models.BooleanField(
                        default=False, help_text="It tells us if the invoice has been already paid or not yet."
                    ),
                ),
                (
                    "buyer",
                    models.ForeignKey(
                        help_text="Company buyer",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="buyer_invoices",
                        to="companies.company",
                    ),
                ),
                (
                    "linked_invoice",
                    models.ForeignKey(
                        blank=True,
                        help_text="An invoice connected with the invoice, e.g. correcting invoice to original.",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="invoices.invoice",
                    ),
                ),
                (
                    "seller",
                    models.ForeignKey(
                        help_text="Company seller",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="seller_invoices",
                        to="companies.company",
                    ),
                ),
            ],
        ),
    ]
