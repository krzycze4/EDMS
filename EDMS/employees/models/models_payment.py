from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Payment(models.Model):
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fee = models.IntegerField(validators=[MinValueValidator(1)])
