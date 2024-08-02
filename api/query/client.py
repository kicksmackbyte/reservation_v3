from typing import Any, Iterable, List, Optional

import graphene
from promise import Promise
from reservation.models import Client


class ClientType(graphene.ObjectType):

    class Meta:
        interfaces = (graphene.Node, )

    first_name = graphene.String()
    last_name = graphene.String()

    providers = graphene.ConnectionField('api.query.provider.ProviderConnection')

    reserved_appointments = graphene.ConnectionField('api.query.appointment.AppointmentConnection')
    confirmed_appointments = graphene.ConnectionField('api.query.appointment.AppointmentConnection')


    @staticmethod
    def resolve_first_name(root: Any, info: graphene.ResolveInfo) -> graphene.String:
        return root.first_name


    @staticmethod
    def resolve_last_name(root: Any, info: graphene.ResolveInfo) -> graphene.String:
        return root.last_name


    @staticmethod
    def resolve_providers(root: Any, info: graphene.ResolveInfo) -> graphene.Field:

        appointment_ids = info.context.loaders.client_confirmed_appointments.load(root.id)
        confirmed_appointments = appointment_ids.then(lambda res: [info.context.loaders.appointment.load(id_) for id_ in res])

        provider_ids = confirmed_appointments.then(lambda res: [r.provider_id for r in res])
        providers = provider_ids.then(lambda res: [info.context.loaders.provider.load(id_) for id_ in res])

        return providers.get()


    @staticmethod
    def resolve_reserved_appointments(root: Any, info: graphene.ResolveInfo) -> graphene.Field:

        appointment_ids = info.context.loaders.client_reserved_appointments.load(root.id)
        appointments = appointment_ids.then(lambda res: [info.context.loaders.appointment.load(id_) for id_ in res])

        return appointments.get()


    @staticmethod
    def resolve_confirmed_appointments(root: Any, info: graphene.ResolveInfo) -> graphene.Field:

        appointment_ids = info.context.loaders.client_confirmed_appointments.load(root.id)
        appointments = appointment_ids.then(lambda res: [info.context.loaders.appointment.load(id_) for id_ in res])

        return appointments.get()


    @classmethod
    def is_type_of(cls, root: Any, info: graphene.ResolveInfo) -> bool:
        return isinstance(root, Client)


    @classmethod
    def get_node(cls, info: graphene.ResolveInfo, decoded_id: str) -> Promise[Optional[Any]]:
        key = int(decoded_id)
        return info.context.loaders.client.load(key)


class ClientConnection(graphene.Connection):

    class Meta:
        node = ClientType


class Query(graphene.ObjectType):

    client = graphene.Node.Field(ClientType)
    clients = graphene.ConnectionField(ClientConnection)


    @staticmethod
    def resolve_clients(root: None, info: graphene.ResolveInfo, **kwargs) -> Iterable[Any]:
        return Client.objects.all()
