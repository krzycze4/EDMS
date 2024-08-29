import factory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from employees.factories.factories_agreement import AgreementFactory
from employees.models.models_termination import Termination
from factory.django import DjangoModelFactory


class TerminationFactory(DjangoModelFactory):
    class Meta:
        model = Termination

    name = factory.Sequence(lambda n: f"Termination #{n + 1}")
    agreement = factory.SubFactory(AgreementFactory)
    create_date = timezone.now().date() + timezone.timedelta(days=100)
    end_date = timezone.now().date() + timezone.timedelta(days=130)
    scan = factory.LazyAttribute(
        lambda _: SimpleUploadedFile("the_file.pdf", b"file_content", content_type="application/pdf")
    )
