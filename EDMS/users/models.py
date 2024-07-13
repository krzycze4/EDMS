from __future__ import annotations

import unicodedata
from typing import Any

from companies.models import Address
from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(UserManager):
    def _create_user(self, email: str, password: str, **extra_fields) -> User:
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel: Any = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        email = GlobalUserModel.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields) -> User:
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields) -> User:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")

        return self._create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email: str) -> User:
        return self.get(**{self.model.EMAIL_FIELD: email})


class User(AbstractUser):
    username_validator = None
    username = None
    first_name = models.CharField(_("first name"), max_length=150, help_text="User's first name.")
    last_name = models.CharField(_("last name"), max_length=150, help_text="User's last name.")
    email = models.EmailField(_("email address"), unique=True, help_text="User's email.")
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. " "Unselect this instead of deleting accounts."
        ),
    )
    phone_number = models.CharField(max_length=50, null=True, help_text="User's phone number, e.g. 48123123123.")
    position = models.CharField(max_length=30, null=True, help_text="User's position, e.g. accountant")
    vacation_days_per_year = models.PositiveSmallIntegerField(
        default=26, help_text="Number of vacation days which owed to the user per year."
    )
    vacation_left = models.SmallIntegerField(default=0, help_text="Number of vacation days which left for the user.")
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, blank=True, help_text="Place of residence of the user."
    )
    photo = models.ImageField(upload_to="photos", default="photos/undraw_profile.svg", help_text="User's face.")

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        swappable = "AUTH_USER_MODEL"

    def get_username(self) -> str:
        """Return the email for this User."""
        return getattr(self, self.EMAIL_FIELD)

    def clean(self) -> None:
        setattr(self, self.EMAIL_FIELD, self.normalize_username(self.get_username()))

    @classmethod
    def normalize_username(cls, email: str) -> str:
        return unicodedata.normalize("NFKC", email) if isinstance(email, str) else email

    @classmethod
    def normalize_email(cls, email: str) -> str:
        return unicodedata.normalize("NFKC", email) if isinstance(email, str) else email

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
