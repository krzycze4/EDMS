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
        User, on_delete=models.CASCADE, related_name="leave_user"
    )
    substitute_users = models.ManyToManyField(User, related_name="substitute_users")
    scan = models.FileField(upload_to="vacations")
    days_off = models.PositiveSmallIntegerField()
