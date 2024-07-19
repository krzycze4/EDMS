# Generated by Django 4.2.11 on 2024-07-16 14:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("companies", "0002_alter_address_city_alter_address_country_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("contracts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="contract",
            name="employee",
            field=models.ManyToManyField(
                help_text="The employees responsible for the contact.",
                related_name="contracts",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="contract",
            name="company",
            field=models.ForeignKey(
                help_text="Company concerned by the contract.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="contracts",
                to="companies.company",
            ),
        ),
        migrations.AlterField(
            model_name="contract",
            name="create_date",
            field=models.DateField(help_text="Creation date of the contract."),
        ),
        migrations.AlterField(
            model_name="contract",
            name="end_date",
            field=models.DateField(help_text="Last day of the contract."),
        ),
        migrations.AlterField(
            model_name="contract",
            name="name",
            field=models.CharField(help_text="Contract name, e.g. Contract #PLAY-01/01/2024", max_length=25),
        ),
        migrations.AlterField(
            model_name="contract",
            name="price",
            field=models.PositiveIntegerField(help_text="The whole net income from the contract."),
        ),
        migrations.AlterField(
            model_name="contract",
            name="scan",
            field=models.FileField(help_text="The physical version of the contract.", upload_to="contracts/"),
        ),
        migrations.AlterField(
            model_name="contract",
            name="start_date",
            field=models.DateField(help_text="First day of the contract."),
        ),
        migrations.AlterUniqueTogether(
            name="contract",
            unique_together={("name", "create_date", "start_date", "end_date", "company", "price")},
        ),
    ]
