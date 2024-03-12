# Generated by Django 5.0.1 on 2024-02-13 15:29

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("companies", "0001_initial"),
        ("contracts", "0001_initial"),
        ("invoices", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Protocol",
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
                ("name", models.CharField(max_length=64)),
                ("scan", models.FileField(upload_to="protocols/")),
                ("create_date", models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name="Order",
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
                ("name", models.CharField(max_length=15)),
                (
                    "payment",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=8,
                        validators=[django.core.validators.MinValueValidator(1.0)],
                        verbose_name="Payment net price",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("open", "open"),
                            ("invoicing", "invoicing"),
                            ("closed", "closed"),
                        ],
                        default="open",
                        max_length=9,
                    ),
                ),
                ("create_date", models.DateField(default=django.utils.timezone.now)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("description", models.TextField(blank=True)),
                (
                    "company",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="orders",
                        to="companies.company",
                    ),
                ),
                (
                    "contract",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="orders",
                        to="contracts.contract",
                    ),
                ),
                (
                    "cost_invoice",
                    models.ManyToManyField(
                        blank=True,
                        related_name="orders_from_cost_invoice",
                        to="invoices.invoice",
                    ),
                ),
                (
                    "invoice",
                    models.ManyToManyField(
                        blank=True,
                        related_name="orders_from_income_invoice",
                        to="invoices.invoice",
                    ),
                ),
            ],
        ),
    ]
