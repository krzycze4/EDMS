from django.db import models


class Address(models.Model):
    street_name = models.CharField(max_length=100)
    street_number = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    postcode = models.CharField(max_length=10)
    country = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.street_name} {self.street_number}\n{self.postcode} {self.city}\n{self.country}"

    class Meta:
        verbose_name_plural = "Addresses"


class Company(models.Model):
    name = models.CharField(max_length=100, verbose_name="Company Name")
    KRS_id = models.BigIntegerField(verbose_name="KRS Number")
    REGON_id = models.BigIntegerField(verbose_name="REGON Number")
    NIP_id = models.BigIntegerField(verbose_name="NIP Number")
    address = models.ForeignKey(
        Address, default=None, on_delete=models.SET_DEFAULT, null=True
    )
    is_mine = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Companies"
