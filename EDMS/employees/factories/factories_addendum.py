from datetime import timedelta

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

    name = Sequence(lambda n: f"Addendum #{n + 1}")
    agreement = factory.SubFactory(AgreementFactory)
    create_date = factory.LazyAttribute(lambda obj: obj.agreement.end_date - timedelta(days=1))
    end_date = factory.LazyAttribute(lambda obj: obj.agreement.end_date + timedelta(days=365))
    salary_gross = Decimal(6000)
    scan = factory.LazyAttribute(
        lambda _: SimpleUploadedFile("the_file.pdf", b"file_content", content_type="application/pdf")
    )
