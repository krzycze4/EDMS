# Generated by Django 5.0.1 on 2024-02-08 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Addendum",
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
                ("end_date", models.DateField()),
                ("salary_gross", models.PositiveSmallIntegerField()),
                ("scan", models.FileField(upload_to="addenda")),
            ],
            options={
                "verbose_name_plural": "Addenda",
            },
        ),
        migrations.CreateModel(
            name="Agreement",
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
                ("name", models.CharField(max_length=25, unique=True)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("employment contract", "employment contract"),
                            ("commission agreement", "commission agreement"),
                            ("contract of mandate", "contract of mandate"),
                            ("B2B", "B2B"),
                        ],
                        max_length=20,
                    ),
                ),
                ("salary_gross", models.IntegerField()),
                ("create_date", models.DateField()),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("end_date_actual", models.DateField()),
                ("scan", models.FileField(upload_to="agreements")),
                ("is_current", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Termination",
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
                ("end_date", models.DateField()),
                ("scan", models.FileField(upload_to="terminations/")),
            ],
        ),
        migrations.CreateModel(
            name="Vacation",
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
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("annual", "annual"),
                            ("maternity", "maternity"),
                            ("parental", "parental"),
                            ("childcare", "childcare"),
                            ("special", "special"),
                            ("sick", "sick"),
                            ("unpaid", "unpaid"),
                        ],
                        max_length=9,
                    ),
                ),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("scan", models.FileField(upload_to="vacations")),
            ],
        ),
    ]