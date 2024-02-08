from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Agreement(models.Model):
    EMPLOYMENT = "employment contract"
    COMMISSION = "commission agreement"
    MANDATE = "contract of mandate"
    B2B = "B2B"
    TYPE_CHOICES = [
        (EMPLOYMENT, EMPLOYMENT),
        (COMMISSION, COMMISSION),
        (MANDATE, MANDATE),
        (B2B, B2B),
    ]
    name = models.CharField(max_length=25, unique=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    salary_gross = models.IntegerField()
    create_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField(help_text="Date in agreement scan.")
    end_date_actual = models.DateField(
        help_text="Calculated date after adding addenda or termination. Necessary to calculate vacations for employee."
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    scan = models.FileField(upload_to="agreements")
    is_current = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.set_end_date_actual()
        self.set_is_current()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.user.vacation_left = 0
        self.user.save()
        super().delete(*args, **kwargs)

    def set_end_date_actual(self) -> None:
        if not self.pk:
            self.end_date_actual = self.end_date
        else:
            if not (self.addendum_set.exists() or hasattr(self, "termination")):
                self.end_date_actual = self.end_date

    def set_is_current(self) -> None:
        if self.end_date_actual < timezone.now().date():
            self.is_current = False
        else:
            self.is_current = True
