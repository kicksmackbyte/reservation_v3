from django.test import TestCase
from django.utils import timezone

import graphene

from api.query.appointment import Query
from tests.api.utils import connection_to_list, request_with_loaders
from reservation.models import Appointment, Provider, Reservation

from examples.queries import AvailableAppointments

import datetime
from model_bakery import baker


class TestAvailableAppointmentsQuery(TestCase):


    def setUp(self):

        self.schema = graphene.Schema(query=Query)
        self.request = request_with_loaders()

        self.provider = baker.make(Provider)


    def test_available_appointments_query(self):

        appointments = []

        self.now = timezone.now() + datetime.timedelta(hours=25)
        for slot_num in range(10):

            offset = slot_num * 15
            time_slot = self.now + datetime.timedelta(minutes=offset)

            appointment = Appointment(time_slot=time_slot, provider=self.provider)
            appointments.append(appointment)

        Appointment.objects.bulk_create(appointments)

        result = self.schema.execute(AvailableAppointments, context=self.request)
        self.assertIsNone(result.errors, msg='Errors prevented execution for %s' % AvailableAppointments)

        available_appointments = connection_to_list(result.data['availableAppointments'])
        self.assertTrue(len(available_appointments) == 10)


    def test_available_appointments_some_expired_query(self):

        appointments = []

        self.now = timezone.now() + datetime.timedelta(hours=22, minutes=59)
        for slot_num in range(10):

            offset = slot_num * 15
            time_slot = self.now + datetime.timedelta(minutes=offset)

            appointment = Appointment(time_slot=time_slot, provider=self.provider)
            appointments.append(appointment)

        Appointment.objects.bulk_create(appointments)

        result = self.schema.execute(AvailableAppointments, context=self.request)
        self.assertIsNone(result.errors, msg='Errors prevented execution for %s' % AvailableAppointments)

        available_appointments = connection_to_list(result.data['availableAppointments'])
        self.assertTrue(len(available_appointments) == 5)


    def test_available_appointments_some_reserved_query(self):

        appointments = []

        self.now = timezone.now() + datetime.timedelta(hours=25)
        for slot_num in range(10):

            offset = slot_num * 15
            time_slot = self.now + datetime.timedelta(minutes=offset)

            appointment = Appointment(time_slot=time_slot, provider=self.provider)
            appointments.append(appointment)

        appointment_objs = Appointment.objects.bulk_create(appointments)


        for i in range(10):
            if (i % 2) == 0:
               baker.make(Reservation, confirmed=True, appointment=appointment_objs[i])

        result = self.schema.execute(AvailableAppointments, context=self.request)
        self.assertIsNone(result.errors, msg='Errors prevented execution for %s' % AvailableAppointments)

        available_appointments = connection_to_list(result.data['availableAppointments'])
        self.assertTrue(len(available_appointments) == 5)
