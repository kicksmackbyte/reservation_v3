from django.test import TestCase
from django.utils import timezone

import graphene
from graphql.error.located_error import GraphQLLocatedError

from api.mutation.reservation import Mutation
from tests.api.utils import request_with_loaders

from examples.mutations import ReservationCreate, ReservationConfirm
from reservation.models import Appointment, Client, Reservation

import datetime
from model_bakery import baker

from api.utils import to_global_id


class TestAppointmentMutation(TestCase):

    def setUp(self):

        self.schema = graphene.Schema(mutation=Mutation)
        self.request = request_with_loaders()

        client = baker.make(Client)
        self.client_id = to_global_id('ClientType', client.id)

        self.expired_time_slot = timezone.now()
        self.expired_appointment = baker.make(Appointment, time_slot=self.expired_time_slot)
        self.expired_appointment_id = to_global_id('AppointmentType', self.expired_appointment.id)

        available_time_slot = timezone.now() + datetime.timedelta(hours=25)
        self.available_appointment = baker.make(Appointment, time_slot=available_time_slot)
        self.available_appointment_id = to_global_id('AppointmentType', self.available_appointment.id)


    def test_create_reservation(self):

        '''Happy path

        '''

        variables = {
            'input': {
                'clientId': self.client_id,
                'appointmentId': self.available_appointment_id,
            }
        }

        result = self.schema.execute(ReservationCreate, context=self.request, variables=variables)
        self.assertIsNone(result.errors, msg='Errors prevented execution for %s' % ReservationCreate)


    def test_create_expired_reservation(self):

        '''Expired reservation

        '''

        variables = {
            'input': {
                'clientId': self.client_id,
                'appointmentId': self.expired_appointment_id,
            }
        }

        result = self.schema.execute(ReservationCreate, context=self.request, variables=variables)
        self.assertTrue(result.errors)

        error_type = type(result.errors[0])
        self.assertEquals(error_type, GraphQLLocatedError)


    def test_create_unavailable_reservation(self):

        '''Appointment already taken

        '''

        variables = {
            'input': {
                'clientId': self.client_id,
                'appointmentId': self.available_appointment_id,
            }
        }

        result = self.schema.execute(ReservationCreate, context=self.request, variables=variables)
        self.assertIsNone(result.errors, msg='Errors prevented execution for %s' % ReservationCreate)

        result = self.schema.execute(ReservationCreate, context=self.request, variables=variables)
        self.assertTrue(result.errors)

        error_type = type(result.errors[0])
        self.assertEquals(error_type, GraphQLLocatedError)


    def test_confirm_reservation(self):

        '''Happy path

        '''
        reservation = baker.make(Reservation, appointment=self.available_appointment)
        reservation_id = to_global_id('ReservationType', reservation.id)

        variables = {
            'input': {
                'reservationId': reservation_id,
            }
        }

        result = self.schema.execute(ReservationConfirm, context=self.request, variables=variables)
        self.assertIsNone(result.errors, msg='Errors prevented execution for %s' % ReservationConfirm)


    def test_confirm_expired_reservation(self):

        '''Reservation has expired

        '''
        reservation = baker.make(Reservation, appointment=self.available_appointment, expiry=self.expired_time_slot)
        reservation_id = to_global_id('ReservationType', reservation.id)

        variables = {
            'input': {
                'reservationId': reservation_id,
            }
        }

        result = self.schema.execute(ReservationConfirm, context=self.request, variables=variables)
        self.assertTrue(result.errors)

        error_type = type(result.errors[0])
        self.assertEquals(error_type, GraphQLLocatedError)
