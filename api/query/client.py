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

    reservations = graphene.ConnectionField('api.query.reservation.ReservationConnection')
    active_reservations = graphene.ConnectionField('api.query.reservation.ReservationConnection')
    confirmed_reservations = graphene.ConnectionField('api.query.reservation.ReservationConnection')
    expired_reservations = graphene.ConnectionField('api.query.reservation.ReservationConnection')


    @staticmethod
    def resolve_first_name(root: Any, info: graphene.ResolveInfo) -> graphene.String:
        return root.first_name


    @staticmethod
    def resolve_last_name(root: Any, info: graphene.ResolveInfo) -> graphene.String:
        return root.last_name


    @staticmethod
    def resolve_providers(root: Any, info: graphene.ResolveInfo) -> graphene.Field:

        reservations = info.context.loaders.reservations_from_client.load(root.id)

        appointment_ids = reservations.then(lambda res: [r.appointment_id for r in res])
        appointments = appointment_ids.then(lambda res: [info.context.loaders.appointment.load(id_) for id_ in res])

        provider_ids = appointments.then(lambda res: [r.provider_id for r in res])
        providers = provider_ids.then(lambda res: [info.context.loaders.provider.load(id_) for id_ in res])

        return providers


    @staticmethod
    def resolve_reservations(root: Any, info: graphene.ResolveInfo) -> graphene.Field:
        return info.context.loaders.reservations_from_client.load(root.id)


    @staticmethod
    def resolve_active_reservations(root: Any, info: graphene.ResolveInfo) -> graphene.Field:
        return info.context.loaders.active_reservations_from_client.load(root.id)


    @staticmethod
    def resolve_confirmed_reservations(root: Any, info: graphene.ResolveInfo) -> graphene.Field:
        return info.context.loaders.confirmed_reservations_from_client.load(root.id)


    @staticmethod
    def resolve_expired_reservations(root: Any, info: graphene.ResolveInfo) -> graphene.Field:
        return info.context.loaders.expired_reservations_from_client.load(root.id)


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
