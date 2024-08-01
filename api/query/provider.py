from typing import Any, Iterable, List, Optional

import graphene
from promise import Promise
from reservation.models import Provider


class ProviderType(graphene.ObjectType):

    class Meta:
        interfaces = (graphene.Node, )

    first_name = graphene.String()
    last_name = graphene.String()

    available_appointments = graphene.Field('api.query.appointment.AppointmentConnection')
    reserved_appointments = graphene.Field('api.query.appointment.AppointmentConnection')

    schedule = graphene.Field('api.query.appointment.AppointmentConnection')


    @staticmethod
    def resolve_first_name(root: Any, info: graphene.ResolveInfo) -> graphene.String:
        return root.first_name


    @staticmethod
    def resolve_last_name(root: Any, info: graphene.ResolveInfo) -> graphene.String:
        return root.last_name


    @staticmethod
    def resolve_available_appointments(root: Any, info: graphene.ResolveInfo) -> graphene.Field:
        return info.context.loaders.provider_available_appointments.load(key)


    @staticmethod
    def resolve_reserved_appointments(root: Any, info: graphene.ResolveInfo) -> graphene.Field:
        return info.context.loaders.provider_reserved_appointments.load(key)


    @staticmethod
    def resolve_schedule(root: Any, info: graphene.ResolveInfo) -> graphene.Field:
        return info.context.loaders.provider_schedule.load(key)


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
