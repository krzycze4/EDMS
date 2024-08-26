from decimal import Decimal

import factory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from employees.models.models_agreement import Agreement
from factory.django import DjangoModelFactory
from users.factories import UserFactory


class AgreementFactory(DjangoModelFactory):
    class Meta:
        model = Agreement

    name = factory.Sequence(lambda n: f"Agreement #{n + 1}")
    type = "employment contract"
    salary_gross = Decimal(5000)
    create_date = factory.LazyFunction(lambda: timezone.now().date() - timezone.timedelta(days=1))
    start_date = factory.LazyFunction(lambda: timezone.now().date())
    end_date = factory.LazyFunction(lambda: timezone.now().date() + timezone.timedelta(days=365))
    end_date_actual = factory.LazyAttribute(lambda obj: obj.end_date)
    user = factory.SubFactory(UserFactory)
    scan = factory.LazyAttribute(
        lambda _: SimpleUploadedFile("the_file.pdf", b"file_content", content_type="application/pdf")
    )
    is_current = True
