from django.test import TestCase
from model_bakery import baker

from reservation.models import Reservation


class ReservationModelTestCase(TestCase):

    def setUp(self):
        self.reservation = baker.make(Reservation)


    def test_the_thing(self):
        self.assertIsInstance(self.reservation, Reservation)
