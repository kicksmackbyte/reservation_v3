from django.test import TestCase
import graphene

from api.mutation.provider import Mutation
from tests.api.utils import request_with_loaders

from examples.mutations import ProviderCreate


class TestProviderMutation(TestCase):

    def setUp(self):

        self.schema = graphene.Schema(mutation=Mutation)
        self.request = request_with_loaders()


    def test_create_provider(self):

        variables = {
            'input': {
                'firstName': 'Dr. Henry',
                'lastName': 'Meds',
            }
        }

        result = self.schema.execute(ProviderCreate, context=self.request, variables=variables)
        self.assertIsNone(result.errors, msg='Errors prevented execution for %s' % ProviderCreate)
