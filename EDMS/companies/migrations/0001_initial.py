# Generated by Django 4.2.6 on 2023-11-22 19:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Address",
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
                ("street_name", models.CharField(max_length=100)),
                ("street_number", models.CharField(max_length=10)),
                ("city", models.CharField(max_length=50)),
                ("postcode", models.CharField(max_length=10)),
                ("country", models.CharField(max_length=50)),
            ],
            options={
                "verbose_name_plural": "Addresses",
            },
        ),
        migrations.CreateModel(
            name="Company",
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
                ("name", models.CharField(max_length=100, verbose_name="Company Name")),
                ("krs", models.BigIntegerField(verbose_name="KRS Number")),
                ("regon", models.BigIntegerField(verbose_name="REGON Number")),
                ("nip", models.BigIntegerField(verbose_name="NIP Number")),
                ("is_mine", models.BooleanField(default=False)),
                (
                    "address",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="companies.address",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Companies",
            },
        ),
    ]
