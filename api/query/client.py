from typing import Any, Iterable, List, Optional

import graphene
from promise import Promise
from reservation.models import Client


class ClientType(graphene.ObjectType):

    class Meta:
        interfaces = (graphene.Node, )

    first_name = graphene.String()

    reserved_appointments = graphene.Field('api.query.appointment.AppointmentConnection')


    @staticmethod
    def resolve_first_name(root: Any, info: graphene.ResolveInfo) -> graphene.String:
        return root.first_name


    @staticmethod
    def resolve_reserved_appointments(root: Any, info: graphene.ResolveInfo) -> graphene.Field:
        return info.context.loaders.client_reserved_appointments.load(root.id)


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
