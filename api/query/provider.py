from typing import Any, Iterable, List, Optional

import graphene
from promise import Promise
from reservation.models import Provider


class ProviderType(graphene.ObjectType):

    class Meta:
        interfaces = (graphene.Node, )

    first_name = graphene.String()
    last_name = graphene.String()

    clients = graphene.ConnectionField('api.query.client.ClientConnection')

    appointments = graphene.ConnectionField('api.query.appointment.AppointmentConnection')

    available_appointments = graphene.ConnectionField('api.query.appointment.AppointmentConnection')
    confirmed_appointments = graphene.ConnectionField('api.query.appointment.AppointmentConnection')
    reserved_appointments = graphene.ConnectionField('api.query.appointment.AppointmentConnection')


    @staticmethod
    def resolve_first_name(root: Any, info: graphene.ResolveInfo) -> graphene.String:
        return root.first_name


    @staticmethod
    def resolve_last_name(root: Any, info: graphene.ResolveInfo) -> graphene.String:
        return root.last_name


    @staticmethod
    def resolve_clients(root: Any, info: graphene.ResolveInfo) -> graphene.Field:

        reservations = info.context.loaders.reservations_from_provider.load(root.id)
        client_ids = reservations.then(lambda res: [r.client_id for r in res])
        clients = client_ids.then(lambda res: [info.context.loaders.client.load(id_) for id_ in res])

        return clients


    @staticmethod
    def resolve_appointments(root: Any, info: graphene.ResolveInfo) -> graphene.Field:
        return info.context.loaders.appointments_from_provider.load(root.id)


    @staticmethod
    def resolve_available_appointments(root: Any, info: graphene.ResolveInfo) -> graphene.Field:
        return info.context.loaders.available_appointments_from_provider.load(root.id)


    @staticmethod
    def resolve_confirmed_appointments(root: Any, info: graphene.ResolveInfo) -> graphene.Field:
        return info.context.loaders.confirmed_appointments_from_provider.load(root.id)


    @staticmethod
    def resolve_reserved_appointments(root: Any, info: graphene.ResolveInfo) -> graphene.Field:
        return info.context.loaders.reserved_appointments_from_provider.load(root.id)


    @classmethod
    def is_type_of(cls, root: Any, info: graphene.ResolveInfo) -> bool:
        return isinstance(root, Provider)


    @classmethod
    def get_node(cls, info: graphene.ResolveInfo, decoded_id: str) -> Promise[Optional[Any]]:
        key = int(decoded_id)
        return info.context.loaders.provider.load(key)


class ProviderConnection(graphene.Connection):

    class Meta:
        node = ProviderType


class Query(graphene.ObjectType):

    provider = graphene.Node.Field(ProviderType)
    providers = graphene.ConnectionField(ProviderConnection)


    @staticmethod
    def resolve_providers(root: None, info: graphene.ResolveInfo, **kwargs) -> Iterable[Any]:
        return Provider.objects.all()
