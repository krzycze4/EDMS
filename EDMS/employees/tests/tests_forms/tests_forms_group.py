from django.contrib.auth.models import Group
from django.test import TestCase
from employees.forms.forms_group import GroupForm
from users.factories import UserFactory


class GroupFormTests(TestCase):
    def setUp(self) -> None:
        self.group1 = Group.objects.create(name="Group1")
        self.group2 = Group.objects.create(name="Group2")
        self.user = UserFactory.create()
        self.user.groups.add(self.group1)

    def test_if_form_is_valid(self):
        form_data = {"groups": [self.group1, self.group2]}
        form = GroupForm(data=form_data)
        self.assertTrue(form.is_valid())
