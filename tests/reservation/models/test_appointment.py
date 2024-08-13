from django.test import TestCase
from model_bakery import baker

from reservation.models import Appointment


class AppointmentModelTestCase(TestCase):

    def setUp(self):
        self.appointment = baker.make(Appointment)


    def test_the_thing(self):
        self.assertIsInstance(self.appointment, Appointment)
