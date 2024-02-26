from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Vacation(models.Model):
    ANNUAL = "annual"
    MATERNITY = "maternity"
    PARENTAL = "parental"
    CHILDCARE = "childcare"
    SPECIAL = "special"
    SICK = "sick"
    UNPAID = "unpaid"
    TYPE_CHOICES = [
        (ANNUAL, ANNUAL),
        (MATERNITY, MATERNITY),
        (PARENTAL, PARENTAL),
        (CHILDCARE, CHILDCARE),
        (SPECIAL, SPECIAL),
        (SICK, SICK),
        (UNPAID, UNPAID),
    ]
    type = models.CharField(max_length=9, choices=TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    leave_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="vacations"
    )
    substitute_users = models.ManyToManyField(User, related_name="vacation")
    scan = models.FileField(upload_to="vacations")
    included_days_off = models.PositiveSmallIntegerField(
        help_text="If you take vacations and there are included days off (for example weekend) then you set "
        "included_days_off as 2 to count properly."
    )

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        self.count_vacation_left()

    def delete(self, *args, **kwargs) -> None:
        super().delete(*args, **kwargs)
        self.count_vacation_left()

    def count_vacation_left(self) -> None:
        from employees.models.models_agreement import (  # Because of Circular Import
            Agreement,
        )

        agreement = (
            self.leave_user.agreements.filter(type=Agreement.EMPLOYMENT)
            .order_by("-create_date")
            .first()
        )
        self.leave_user.vacation_left = (
            agreement.count_granted_vacation_from_agreement()
            - self.count_used_vacation()
        )
        self.leave_user.save()

    @staticmethod
    def count_used_vacation() -> int:
        used_vacation_days: int = 0
        vacations = list(Vacation.objects.filter(type=Vacation.ANNUAL))
        for vacation in vacations:
            used_vacation_days += (
                (vacation.end_date - vacation.start_date).days
                - vacation.included_days_off
                + 1
            )
        return used_vacation_days
