from django.test import TestCase
from django.utils import timezone

import graphene

from api.query.appointment import Query
from tests.api.utils import connection_to_list, request_with_loaders
from reservation.models import Appointment, Provider

from examples.queries import AvailableAppointments

import datetime
from model_bakery import baker


class TestAvailableAppointmentsQuery(TestCase):


    def setUp(self):

        self.schema = graphene.Schema(query=Query)
        self.request = request_with_loaders()

        provider = baker.make(Provider)
        appointments = []

        self.now = timezone.now() + datetime.timedelta(hours=22, minutes=59)
        for slot_num in range(10):

            offset = slot_num * 15
            time_slot = self.now + datetime.timedelta(minutes=offset)

            appointment = Appointment(time_slot=time_slot, provider=provider)
            appointments.append(appointment)

        Appointment.objects.bulk_create(appointments)


    def test_available_appointments_query(self):

        result = self.schema.execute(AvailableAppointments, context=self.request)
        self.assertIsNone(result.errors, msg='Errors prevented execution for %s' % AvailableAppointments)

        available_appointments = connection_to_list(result.data['availableAppointments'])
        self.assertTrue(len(available_appointments) == 5)
