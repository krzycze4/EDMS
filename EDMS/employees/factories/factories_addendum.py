import secrets
from datetime import date, timedelta

import factory
from _decimal import Decimal
from django.core.files.uploadedfile import SimpleUploadedFile
from employees.factories.factories_agreement import AgreementFactory
from employees.models.models_addendum import Addendum
from factory import Sequence
from factory.django import DjangoModelFactory


class AddendumFactory(DjangoModelFactory):
    class Meta:
        model = Addendum

    name = Sequence(lambda n: f"Addendum #{n}")
    agreement = factory.SubFactory(AgreementFactory)
    salary_gross = Decimal(6000)
    scan = factory.LazyAttribute(
        lambda _: SimpleUploadedFile("the_file.pdf", b"file_content", content_type="application/pdf")
    )

    @factory.lazy_attribute
    def create_date(self) -> date:
        duration_agreement_in_days = self.agreement.end_date - self.agreement.start_date + timedelta(days=1)
        return self.agreement.start_date + timedelta(days=secrets.randbelow(int(duration_agreement_in_days.days)))

    @factory.lazy_attribute
    def end_date(self) -> date:
        return self.agreement.end_date + timedelta(days=secrets.randbelow(366))
