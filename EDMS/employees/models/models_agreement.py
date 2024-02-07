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
    end_date = models.DateField()
    end_date_actual = models.DateField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    scan = models.FileField(upload_to="agreements")
    is_current = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.set_end_date_actual()
        self.set_is_current()
        self.set_vacation_left()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.user.vacation_left = 0
        self.user.save()
        super().delete(*args, **kwargs)

    def set_end_date_actual(self) -> None:
        if not self.pk:
            self.end_date_actual = self.end_date
        else:
            has_termination_or_addendum = self.termination or self.addendum_set.exists()
            if not has_termination_or_addendum:
                self.end_date_actual = self.end_date

    def set_is_current(self) -> None:
        if self.end_date_actual < timezone.now().date():
            self.is_current = False
        else:
            self.is_current = True

    def set_vacation_left(self) -> None:
        if self.type == self.EMPLOYMENT:
            current_year = timezone.now().year
            if (
                self.start_date.year == current_year
                and self.end_date_actual.year == current_year
            ):
                months_in_year = 12
                work_month_current_year = (
                    self.end_date_actual.month - self.start_date.month + 1
                )
                self.user.vacation_left = (
                    work_month_current_year
                    * self.user.vacation_days_per_year
                    / months_in_year
                )
                self.user.save()
