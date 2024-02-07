from django.db import models
from django.utils import timezone
from employees.models.models_agreement import Agreement


class Addendum(models.Model):
    name = models.CharField(max_length=25)
    agreement = models.ForeignKey(Agreement, on_delete=models.CASCADE)
    create_date = models.DateField()
    end_date = models.DateField()
    salary_gross = models.PositiveSmallIntegerField()
    scan = models.FileField(upload_to="addenda")

    class Meta:
        verbose_name_plural = "Addenda"

    def __str__(self):
        return f"Addendum #{self.name}"

    def update_agreement_end_date(self):
        last_addendum = (
            Addendum.objects.filter(agreement=self.agreement)
            .order_by("create_date")
            .last()
        )
        if last_addendum:
            self.agreement.end_date_actual = last_addendum.end_date
        else:
            self.agreement.end_date_actual = self.agreement.end_date

    def update_agreement_is_current(self):
        if self.agreement.end_date_actual < timezone.now().date():
            self.agreement.is_current = False
        else:
            self.agreement.is_current = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_agreement_end_date()
        self.update_agreement_is_current()
        self.agreement.save()

    def delete(self, *args, **kwargs):
        agreement = self.agreement
        super().delete(*args, **kwargs)
        last_addendum = (
            Addendum.objects.filter(agreement=agreement).order_by("create_date").last()
        )
        if last_addendum:
            agreement.end_date_actual = last_addendum.end_date
        else:
            agreement.end_date_actual = agreement.end_date
        self.update_agreement_is_current()
        agreement.save()
