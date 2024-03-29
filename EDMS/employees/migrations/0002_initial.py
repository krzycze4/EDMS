# Generated by Django 5.0.1 on 2024-02-13 15:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("employees", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="agreement",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="agreements",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="addendum",
            name="agreement",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="employees.agreement"
            ),
        ),
        migrations.AddField(
            model_name="payment",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="termination",
            name="agreement",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="employees.agreement"
            ),
        ),
        migrations.AddField(
            model_name="vacation",
            name="leave_user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="leave_user",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="vacation",
            name="substitute_users",
            field=models.ManyToManyField(
                related_name="substitute_users", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
