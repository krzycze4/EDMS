from django.test import TestCase
from employees.factories.factories_addendum import AddendumFactory
from employees.models.models_addendum import Addendum


class AddendumFactoryTests(TestCase):
    def test_create_correct_addendum(self):
        AddendumFactory.create()
        self.assertEqual(Addendum.objects.count(), 1)

    def test_create_correct_addendum_bulk(self):
        AddendumFactory.create_batch(10)
        self.assertEqual(Addendum.objects.count(), 10)
