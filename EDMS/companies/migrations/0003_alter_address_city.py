# Generated by Django 4.2.11 on 2024-05-15 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("companies", "0002_alter_contact_phone"),
    ]

    operations = [
        migrations.AlterField(
            model_name="address",
            name="city",
            field=models.CharField(max_length=100),
        ),
    ]
