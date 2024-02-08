# Generated by Django 5.0.1 on 2024-02-08 07:29

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
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, unique=True)),
                (
                    "net_price",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "vat",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "gross",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                ("create_date", models.DateField()),
                ("service_date", models.DateField()),
                ("payment_date", models.DateField()),
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
                        max_length=10,
                    ),
                ),
                ("scan", models.FileField(upload_to="invoices/")),
                ("is_paid", models.BooleanField(default=False)),
                (
                    "buyer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="buyer_invoices",
                        to="companies.company",
                    ),
                ),
                (
                    "linked_invoice",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="invoices.invoice",
                    ),
                ),
                (
                    "seller",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="seller_invoices",
                        to="companies.company",
                    ),
                ),
            ],
        ),
    ]
