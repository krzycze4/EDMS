from django.db import models


class Address(models.Model):
    street_name = models.CharField(max_length=100, help_text="Street name e.g. Warszawska")
    street_number = models.CharField(max_length=10, help_text="Building number/apartment number e.g. 21/37")
    city = models.CharField(max_length=100, help_text="City e.g. Warsaw")
    postcode = models.CharField(max_length=10, help_text="Postcode e.g. 01-234")
    country = models.CharField(max_length=100, help_text="Country e.g. Poland")

    def __str__(self) -> str:
        return f"{self.street_name} {self.street_number}\n{self.postcode} {self.city}\n{self.country}"

    class Meta:
        verbose_name_plural = "Addresses"


class Company(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Company Name",
        help_text="Company name e.g. PLUS SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ",
    )
    krs = models.BigIntegerField(
        verbose_name="KRS Number",
        unique=True,
        help_text="Identifier of company. It's 9 (if company is based in one voivodeship) or 14 (if more than one voivodeship) digits.",
    )
    regon = models.BigIntegerField(
        verbose_name="REGON Number", unique=True, help_text="Identifier of company. It's 9 digits."
    )
    nip = models.BigIntegerField(
        verbose_name="NIP Number", unique=True, help_text="Identifier of company. It's 10 digits."
    )
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, help_text="Address where company is registered in KRS system."
    )
    is_mine = models.BooleanField(
        default=False, blank=True, help_text="Set true if this company is yours, set false if it's not."
    )
    shortcut = models.CharField(max_length=5, unique=True, help_text="Shortcut of the name of the company, e.g. PLUS")

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Companies"


class Contact(models.Model):
    name = models.CharField(max_length=100, help_text="It's person full name, e.g. John Doe")
    email = models.EmailField(max_length=100, blank=True, help_text="Email, e.g. john_doe@gmail.com")
    phone = models.CharField(max_length=25, blank=True, help_text="Phone number, e.g. +48123456789")
    description = models.CharField(
        max_length=200,
        help_text="Description of that person, e.g. position in the company, special signs - generally less or more important information.",
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="contacts",
        help_text="The company for which the contact person works.",
    )

    class Meta:
        unique_together = [["name", "email", "phone", "company"]]

    def __str__(self):
        return f"{self.name}"
