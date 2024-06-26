# Generated by Django 4.2.11 on 2024-05-08 13:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("orders", "0003_alter_protocol_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="protocol",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="protocols",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
