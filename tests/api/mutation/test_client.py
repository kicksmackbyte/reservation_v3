from django.test import TestCase
import graphene

from api.mutation.client import Mutation
from tests.api.utils import request_with_loaders

from examples.mutations import ClientCreate


class TestClientMutation(TestCase):

    def setUp(self):

        self.schema = graphene.Schema(mutation=Mutation)
        self.request = request_with_loaders()


    def test_create_user(self):

        variables = {
            'input': {
                'firstName': 'Alberto',
                'lastName': 'Garcia',
            }
        }

        result = self.schema.execute(ClientCreate, context=self.request, variables=variables)
        self.assertIsNone(result.errors, msg='Errors prevented execution for %s' % ClientCreate)
