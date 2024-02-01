# Generated by Django 5.0.1 on 2024-01-30 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_user_address_alter_user_first_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="agreement",
            name="create_date",
            field=models.DateField(default="2024-01-01"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="agreement",
            name="name",
            field=models.CharField(max_length=25, unique=True),
        ),
    ]