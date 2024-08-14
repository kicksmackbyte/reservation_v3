from django.test import TestCase
from django.utils import timezone

import graphene

from api.query.reservation import Query
from tests.api.utils import connection_to_list, request_with_loaders
from reservation.models import Reservation

from examples.queries import Reservations

import datetime
from model_bakery import baker


class TestReservationsQuery(TestCase):


    def setUp(self):

        self.schema = graphene.Schema(query=Query)
        self.request = request_with_loaders()


    def test_reservations_query(self):

        reservations = []

        expiry = timezone.now() + datetime.timedelta(minutes=15)
        reservation = baker.make(Reservation, expiry=expiry)

        result = self.schema.execute(Reservations, context=self.request)
        self.assertIsNone(result.errors, msg='Errors prevented execution for %s' % Reservations)

        reservations = connection_to_list(result.data['reservations'])
        self.assertTrue(len(reservations) == 1)

        first_reservation = reservations[0]
        self.assertFalse(first_reservation['expired'])
        self.assertFalse(first_reservation['confirmed'])


    def test_reservations_expired_query(self):

        reservations = []

        expiry = timezone.now() - datetime.timedelta(minutes=1)
        reservation = baker.make(Reservation, expiry=expiry)

        result = self.schema.execute(Reservations, context=self.request)
        self.assertIsNone(result.errors, msg='Errors prevented execution for %s' % Reservations)

        reservations = connection_to_list(result.data['reservations'])
        self.assertTrue(len(reservations) == 1)

        first_reservation = reservations[0]
        self.assertTrue(first_reservation['expired'])
        self.assertFalse(first_reservation['confirmed'])


    def test_reservations_confirmed_query(self):

        reservations = []

        reservation = baker.make(Reservation, confirmed=True)

        result = self.schema.execute(Reservations, context=self.request)
        self.assertIsNone(result.errors, msg='Errors prevented execution for %s' % Reservations)

        reservations = connection_to_list(result.data['reservations'])
        self.assertTrue(len(reservations) == 1)

        first_reservation = reservations[0]
        self.assertFalse(first_reservation['expired'])
        self.assertTrue(first_reservation['confirmed'])
