import graphene

from api.utils import from_global_id

from reservation.models import Provider


class ProviderCreateInput(graphene.InputObjectType):

    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)


class ProviderCreate(graphene.Mutation):

    class Arguments:

        input_ = graphene.Argument(ProviderCreateInput, name='input', required=True)

    provider = graphene.Field('api.query.provider.ProviderType')


    @classmethod
    def mutate(cls, root, info, input_):

        provider = Provider.objects.create(**input_)
        return cls(provider=provider)


class Mutation(graphene.ObjectType):
    provider_create = ProviderCreate.Field()
