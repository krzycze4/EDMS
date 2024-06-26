from django.db import models


class Address(models.Model):
    street_name = models.CharField(max_length=100)
    street_number = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)
    country = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.street_name} {self.street_number}\n{self.postcode} {self.city}\n{self.country}"

    class Meta:
        verbose_name_plural = "Addresses"
        unique_together = [["street_name", "street_number", "city", "postcode", "country"]]


class Company(models.Model):
    name = models.CharField(max_length=100, verbose_name="Company Name")
    krs = models.BigIntegerField(verbose_name="KRS Number", unique=True)
    regon = models.BigIntegerField(verbose_name="REGON Number", unique=True)
    nip = models.BigIntegerField(verbose_name="NIP Number", unique=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    is_mine = models.BooleanField(default=False, blank=True)
    shortcut = models.CharField(max_length=5, unique=True)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Companies"


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True)
    phone = models.CharField(max_length=25, blank=True)
    description = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="contacts")

    class Meta:
        unique_together = [["name", "email", "phone", "company"]]

    def __str__(self):
        return f"{self.name}"
