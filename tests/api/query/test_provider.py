from django.test import TestCase
import graphene

from api.query.provider import Query
from tests.api.utils import connection_to_list, request_with_loaders
from reservation.models import Provider

from examples.queries import Providers
from model_bakery import baker


class TestProvidersQuery(TestCase):


    def setUp(self):

        self.schema = graphene.Schema(query=Query)
        self.request = request_with_loaders()

        providers = baker.make(Provider, _quantity=10, _bulk_create=True)


    def test_providers_query(self):

        result = self.schema.execute(Providers, context=self.request)
        self.assertIsNone(result.errors, msg='Errors prevented execution for %s' % Providers)

        providers = connection_to_list(result.data['providers'])
        self.assertTrue(len(providers) == 10)
