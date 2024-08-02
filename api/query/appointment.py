from typing import Any, Iterable, List, Optional

import graphene
from promise import Promise
from reservation.models import Appointment


class AppointmentType(graphene.ObjectType):

    class Meta:
        interfaces = (graphene.Node, )

    time_slot = graphene.DateTime()
    provider = graphene.Field('api.query.provider.ProviderType')

    client = graphene.Field('api.query.client.ClientType')


    @staticmethod
    def resolve_time_slot(root: Any, info: graphene.ResolveInfo) -> graphene.String:
        return root.time_slot


    @staticmethod
    def resolve_provider(root: Any, info: graphene.ResolveInfo) -> graphene.String:
        return info.context.loaders.provider.load(root.provider_id)


    @staticmethod
    def resolve_client(root: Any, info: graphene.ResolveInfo) -> graphene.String:

        reservation = info.context.loaders.confirmed_reservation_from_appointment.load(root.id)
        client = reservation.then(lambda res: info.context.loaders.client.load(res.client_id) if res else None)

        return client


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

    available_appointments = graphene.ConnectionField(AppointmentConnection)
    confirmed_appointments = graphene.ConnectionField(AppointmentConnection)


    @staticmethod
    def resolve_appointments(root: None, info: graphene.ResolveInfo, **kwargs) -> Iterable[Any]:
        return Appointment.objects.all()


    @staticmethod
    def resolve_available_appointments(root: None, info: graphene.ResolveInfo, **kwargs) -> Iterable[Any]:
        return Appointment.available_objects.all()


    @staticmethod
    def resolve_confirmed_appointments(root: None, info: graphene.ResolveInfo, **kwargs) -> Iterable[Any]:
        return Appointment.confirmed_objects.all()
