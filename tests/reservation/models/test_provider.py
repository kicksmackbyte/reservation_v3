from django.test import TestCase
from model_bakery import baker

from reservation.models import Provider


class ProviderModelTestCase(TestCase):

    def setUp(self):
        self.provider = baker.make(Provider)


    def test_the_thing(self):
        self.assertIsInstance(self.provider, Provider)
