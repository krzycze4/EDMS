import factory
from _decimal import Decimal
from companies.factories import CompanyFactory
from contracts.models import Contract
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from factory import Sequence
from factory.django import DjangoModelFactory
from users.factories import UserFactory


class ContractFactory(DjangoModelFactory):
    class Meta:
        model = Contract

    name = Sequence(lambda n: f"contract{n}")
    create_date = timezone.now().date()
    start_date = timezone.now().date()
    end_date = timezone.now().date() + timezone.timedelta(days=365)
    company = factory.SubFactory(CompanyFactory)
    price = Decimal(1000)
    scan = factory.LazyAttribute(
        lambda _: SimpleUploadedFile("the_file.pdf", b"file_content", content_type="application/pdf")
    )

    @factory.post_generation
    def employee(self, create, employees, **kwargs):
        if not create:
            return
        if employees:
            for employee in employees:
                self.employee.add(employee)
        else:
            self.employee.add(UserFactory())
