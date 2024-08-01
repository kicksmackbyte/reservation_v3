from typing import Any, Iterable, List, Optional

import graphene
from promise import Promise
from reservation.models import Appointment


class AppointmentType(graphene.ObjectType):

    class Meta:
        interfaces = (graphene.Node, )

    time_slot = graphene.DateTime()
    provider = graphene.Field('api.query.provider.ProviderType')


    @staticmethod
    def resolve_time_slot(root: Any, info: graphene.ResolveInfo) -> graphene.String:
        return root.time_slot


    @staticmethod
    def resolve_provider(root: Any, info: graphene.ResolveInfo) -> graphene.String:
        return info.context.loaders.provider.load(root.provider_id)


    @classmethod
    def is_type_of(cls, root: Any, info: graphene.ResolveInfo) -> bool:
        return isinstance(root, Appointment)


    @classmethod
    def get_node(cls, info: graphene.ResolveInfo, decoded_id: str) -> Promise[Optional[Any]]:
        key = int(decoded_id)
        return info.context.loaders.appointment.load(key)


class AppointmentConnection(graphene.Connection):

    class Meta:
        node = AppointmentType


class Query(graphene.ObjectType):

    appointment = graphene.Node.Field(AppointmentType)
    appointments = graphene.ConnectionField(AppointmentConnection)


    @staticmethod
    def resolve_appointments(root: None, info: graphene.ResolveInfo, **kwargs) -> Iterable[Any]:
        return Appointment.objects.all()
