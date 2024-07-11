from datetime import timedelta

import factory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from employees.models.models_vacation import Vacation
from factory.django import DjangoModelFactory
from users.factories import UserFactory


class VacationFactory(DjangoModelFactory):
    class Meta:
        model = Vacation

    type = "annual"
    start_date = factory.LazyFunction(lambda: timezone.now().date())
    end_date = factory.LazyAttribute(lambda obj: obj.start_date + timedelta(days=7))
    leave_user = factory.SubFactory(UserFactory)
    substitute_users = factory.SubFactory(UserFactory)
    scan = factory.LazyAttribute(
        lambda _: SimpleUploadedFile("the_file.pdf", b"file_content", content_type="application/pdf")
    )
    included_days_off = 0

    @factory.post_generation
    def substitute_users(self, create, extracted, **kwargs):
        if extracted:
            for user in extracted:
                self.substitute_users.add(user)

        else:
            substitute_user = UserFactory()
            self.substitute_users.add(substitute_user)
