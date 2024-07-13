from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Salary(models.Model):
    date = models.DateField(help_text="The date when salary went out.")
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="salaries",
        help_text="The money went to this employee.",
    )
    fee = models.IntegerField(validators=[MinValueValidator(1)], help_text="It's net money sent to the employee.")

    class Meta:
        verbose_name_plural = "Salaries"
