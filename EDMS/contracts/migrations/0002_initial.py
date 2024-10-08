# Generated by Django 4.2.14 on 2024-08-30 19:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
        migrations.AlterUniqueTogether(
            name="contract",
            unique_together={("name", "create_date", "start_date", "end_date", "company", "price")},
        ),
    ]
