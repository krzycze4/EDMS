from companies.models import Company
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Contract(models.Model):
    name = models.CharField(max_length=25, help_text="Contract name, e.g. Contract #PLAY-01/01/2024")
    create_date = models.DateField(help_text="Creation date of the contract.")
    start_date = models.DateField(help_text="First day of the contract.")
    end_date = models.DateField(help_text="Last day of the contract.")
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        related_name="contracts",
        help_text="Company concerned by the contract.",
    )
    employee = models.ManyToManyField(
        User, related_name="contracts", help_text="The employees responsible for the contact."
    )
    price = models.PositiveIntegerField(help_text="The whole net income from the contract.")
    scan = models.FileField(upload_to="contracts/", help_text="The physical version of the contract.")

    class Meta:
        unique_together = [["name", "create_date", "start_date", "end_date", "company", "price"]]

    def __str__(self) -> str:
        return f"{self.name}"
