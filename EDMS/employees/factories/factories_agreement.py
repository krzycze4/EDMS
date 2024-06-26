import secrets
from datetime import date, timedelta
from decimal import Decimal

import factory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from employees.models.models_agreement import Agreement
from factory.django import DjangoModelFactory
from users.factories import UserFactory

from EDMS.factory_utils import create_string_format_valid_date


class AgreementFactory(DjangoModelFactory):
    class Meta:
        model = Agreement

    name = factory.Sequence(lambda n: f"Agreement #{n}")
    type = "employment contract"
    salary_gross = Decimal(5000)
    start_date = factory.LazyAttribute(lambda obj: create_string_format_valid_date(obj.create_date))
    end_date = factory.LazyAttribute(lambda obj: create_string_format_valid_date(obj.start_date))
    user = factory.SubFactory(UserFactory)
    scan = factory.LazyAttribute(
        lambda _: SimpleUploadedFile("the_file.pdf", b"file_content", content_type="application/pdf")
    )
    is_current = True

    @factory.lazy_attribute
    def create_date(self) -> date:
        return timezone.now().date() - timedelta(days=secrets.randbelow(366))
