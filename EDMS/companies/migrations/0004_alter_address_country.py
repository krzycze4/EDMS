# Generated by Django 4.2.11 on 2024-05-16 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("companies", "0003_alter_address_city"),
    ]

    operations = [
        migrations.AlterField(
            model_name="address",
            name="country",
            field=models.CharField(max_length=100),
        ),
    ]
