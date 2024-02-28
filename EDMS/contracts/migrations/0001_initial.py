# Generated by Django 5.0.1 on 2024-02-13 15:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("companies", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Contract",
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
                ("name", models.CharField(max_length=25)),
                ("create_date", models.DateField()),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("price", models.PositiveIntegerField()),
                ("scan", models.FileField(upload_to="contracts/")),
                (
                    "company",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="contracts",
                        to="companies.company",
                    ),
                ),
            ],
        ),
    ]