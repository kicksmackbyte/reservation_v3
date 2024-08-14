from django.test import TestCase
from django.utils import timezone

import graphene

from api.mutation.appointment import Mutation
from tests.api.utils import request_with_loaders

from examples.mutations import AppointmentBulkCreate
from reservation.models import Provider

import datetime
from model_bakery import baker

from api.utils import to_global_id


class TestAppointmentMutation(TestCase):

    def setUp(self):

        self.schema = graphene.Schema(mutation=Mutation)
        self.request = request_with_loaders()

        provider = baker.make(Provider)
        self.provider_id = to_global_id('ProviderType', provider.id)

        self.now = timezone.now()


    def test_bulk_create_appointments(self):

        '''Happy path; no pre-existing appointments

        '''

        variables = {
            'input': {
                'providerId': self.provider_id,
                'startTime': self.now,
                'endTime': self.now + datetime.timedelta(days=1),
            }
        }

        result = self.schema.execute(AppointmentBulkCreate, context=self.request, variables=variables)
        self.assertIsNone(result.errors, msg='Errors prevented execution for %s' % AppointmentBulkCreate)


    def test_bulk_create_appointments_start_after_end(self):

        '''startTime comes after endTime

        '''

        variables = {
            'input': {
                'providerId': self.provider_id,
                'startTime': self.now + datetime.timedelta(days=1),
                'endTime': self.now,
            }
        }

        result = self.schema.execute(AppointmentBulkCreate, context=self.request, variables=variables)
        self.assertIsNone(result.errors, msg='Errors prevented execution for %s' % AppointmentBulkCreate)


    def test_bulk_create_appointments_short_delta(self):

        '''(startTime - endTime) < 15 minutes
        '''

        variables = {
            'input': {
                'providerId': self.provider_id,
                'startTime': self.now,
                'endTime': self.now + datetime.timedelta(minutes=10),
            }
        }

        result = self.schema.execute(AppointmentBulkCreate, context=self.request, variables=variables)
        self.assertIsNone(result.errors, msg='Errors prevented execution for %s' % AppointmentBulkCreate)


    def test_bulk_create_appointments_past_end(self):

        '''Extend appointments past any pre-existing end times

        '''

        variables = {
            'input': {
                'providerId': self.provider_id,
                'startTime': self.now,
                'endTime': self.now + datetime.timedelta(days=1),
            }
        }

        result = self.schema.execute(AppointmentBulkCreate, context=self.request, variables=variables)
        self.assertIsNone(result.errors, msg='Errors prevented execution for %s' % AppointmentBulkCreate)


        variables = {
            'input': {
                'providerId': self.provider_id,
                'startTime': self.now + datetime.timedelta(days=2),
                'endTime': self.now + datetime.timedelta(days=3),
            }
        }

        result = self.schema.execute(AppointmentBulkCreate, context=self.request, variables=variables)
        self.assertIsNone(result.errors, msg='Errors prevented execution for %s' % AppointmentBulkCreate)


    def test_bulk_create_appointments_before_start(self):

        '''Extend appointments before any pre-existing start times

        '''

        variables = {
            'input': {
                'providerId': self.provider_id,
                'startTime': self.now + datetime.timedelta(days=2),
                'endTime': self.now + datetime.timedelta(days=3),
            }
        }

        result = self.schema.execute(AppointmentBulkCreate, context=self.request, variables=variables)
        self.assertIsNone(result.errors, msg='Errors prevented execution for %s' % AppointmentBulkCreate)


        variables = {
            'input': {
                'providerId': self.provider_id,
                'startTime': self.now,
                'endTime': self.now + datetime.timedelta(days=1),
            }
        }

        result = self.schema.execute(AppointmentBulkCreate, context=self.request, variables=variables)
        self.assertIsNone(result.errors, msg='Errors prevented execution for %s' % AppointmentBulkCreate)


    def test_bulk_create_appointments_exact_overlap(self):

        '''No-op appointments that exactly overlap

        '''

        variables = {
            'input': {
                'providerId': self.provider_id,
                'startTime': self.now,
                'endTime': self.now + datetime.timedelta(days=1),
            }
        }

        result = self.schema.execute(AppointmentBulkCreate, context=self.request, variables=variables)
        self.assertIsNone(result.errors, msg='Errors prevented execution for %s' % AppointmentBulkCreate)

        result = self.schema.execute(AppointmentBulkCreate, context=self.request, variables=variables)
        self.assertIsNone(result.errors, msg='Errors prevented execution for %s' % AppointmentBulkCreate)


    def test_bulk_create_appointments_overlap(self):

        '''Extend appointments that overlap with pre-existing times

        '''

        variables = {
            'input': {
                'providerId': self.provider_id,
                'startTime': self.now + datetime.timedelta(days=1),
                'endTime': self.now + datetime.timedelta(days=2),
            }
        }

        result = self.schema.execute(AppointmentBulkCreate, context=self.request, variables=variables)
        self.assertIsNone(result.errors, msg='Errors prevented execution for %s' % AppointmentBulkCreate)


        variables = {
            'input': {
                'providerId': self.provider_id,
                'startTime': self.now,
                'endTime': self.now + datetime.timedelta(days=3),
            }
        }

        result = self.schema.execute(AppointmentBulkCreate, context=self.request, variables=variables)
        self.assertIsNone(result.errors, msg='Errors prevented execution for %s' % AppointmentBulkCreate)
