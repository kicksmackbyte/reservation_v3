import graphene

from api.utils import from_global_id

from reservation.models import Client


class ClientCreateInput(graphene.InputObjectType):

    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)


class ClientCreate(graphene.Mutation):

    class Arguments:

        input_ = graphene.Argument(ClientCreateInput, name='input', required=True)

    client = graphene.Field('api.query.client.ClientType')


    @classmethod
    def mutate(cls, root, info, input_):

        client = Client.objects.create(**input_)
        return cls(client=client)


class Mutation(graphene.ObjectType):
    client_create = ClientCreate.Field()
