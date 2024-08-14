from django.test import TestCase
import graphene

from api.query.client import Query
from tests.api.utils import connection_to_list, request_with_loaders
from reservation.models import Client

from examples.queries import Clients
from model_bakery import baker


class TestClientsQuery(TestCase):


    def setUp(self):

        self.schema = graphene.Schema(query=Query)
        self.request = request_with_loaders()

        clients = baker.make(Client, _quantity=10, _bulk_create=True)


    def test_clients_query(self):

        result = self.schema.execute(Clients, context=self.request)
        self.assertIsNone(result.errors, msg='Errors prevented execution for %s' % Clients)

        clients = connection_to_list(result.data['clients'])
        self.assertTrue(len(clients) == 10)
