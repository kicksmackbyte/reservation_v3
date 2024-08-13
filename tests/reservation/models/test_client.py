from django.test import TestCase
from model_bakery import baker

from reservation.models import Client


class ClientModelTestCase(TestCase):

    def setUp(self):
        self.client = baker.make(Client)


    def test_the_thing(self):
        self.assertIsInstance(self.client, Client)
