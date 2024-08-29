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
    type = models.CharField(
        max_length=9,
        choices=TYPE_CHOICES,
        help_text="Type of the agreement one of annual, maternity, parental, childcare, special, sick, unpaid.",
    )
    start_date = models.DateField(help_text="First day of the vacation.")
    end_date = models.DateField(help_text="Last day of the vacation.")
    leave_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="vacations", help_text="Employee which is going on vacation."
    )
    substitute_users = models.ManyToManyField(
        User, related_name="vacation", help_text="Employees which will substitute the employee on vacation."
    )
    scan = models.FileField(upload_to="vacations", help_text="Physical version of the addendum.")
    included_days_off = models.PositiveSmallIntegerField(
        help_text="If you take vacations and there are included days off (for example weekend) then you set "
        "included_days_off as 2 to count properly."
    )

    def save(self, *args, **kwargs) -> None:
        """
        Saves the vacation record and updates the remaining vacation days for the employee.

        Args:
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.
        """
        super().save(*args, **kwargs)
        self.count_vacation_left()

    def delete(self, *args, **kwargs) -> None:
        """
        Deletes the vacation record and updates the remaining vacation days for the employee.

        Args:
            *args: Additional arguments.
            **kwargs: Additional keyword arguments.
        """
        super().delete(*args, **kwargs)
        self.count_vacation_left()

    def count_vacation_left(self) -> None:
        """
        Calculates and updates the remaining vacation days for the employee.
        """
        from employees.models.models_agreement import Agreement

        agreement = self.leave_user.agreements.filter(type=Agreement.EMPLOYMENT).order_by("-create_date").first()
        if agreement:
            self.leave_user.vacation_left = (
                agreement.count_granted_vacation_from_agreement() - self.count_used_vacation()
            )
        else:
            self.leave_user.vacation_left = 0
        self.leave_user.save()

    @staticmethod
    def count_used_vacation() -> int:
        """
        Counts the total number of vacation days used by all employees for annual vacations.

        Returns:
            int: The total number of used vacation days.
        """
        used_vacation_days: int = 0
        vacations = list(Vacation.objects.filter(type=Vacation.ANNUAL))
        for vacation in vacations:
            used_vacation_days += (vacation.end_date - vacation.start_date).days - vacation.included_days_off + 1
        return used_vacation_days
