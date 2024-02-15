from companies.models import Company
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Contract(models.Model):
    name = models.CharField(max_length=25)
    create_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True, related_name="contracts"
    )
    employee = models.ManyToManyField(User, related_name="contracts")
    price = models.PositiveIntegerField()
    scan = models.FileField(upload_to="contracts/")

    def __str__(self) -> str:
        return f"{self.name}"
