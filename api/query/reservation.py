from typing import Any, Iterable, List, Optional

import graphene
from promise import Promise
from reservation.models import Reservation


class ReservationType(graphene.ObjectType):

    class Meta:
        interfaces = (graphene.Node, )

    expiry = graphene.DateTime()

    confirmed = graphene.Boolean()
    expired = graphene.Boolean()

    client = graphene.Field('api.query.client.ClientType')
    provider = graphene.Field('api.query.provider.ProviderType')
    appointment = graphene.Field('api.query.appointment.AppointmentType')


    @staticmethod
    def resolve_expiry(root: Any, info: graphene.ResolveInfo) -> graphene.DateTime:
        return root.expiry


    @staticmethod
    def resolve_confirmed(root: Any, info: graphene.ResolveInfo) -> graphene.Boolean:
        return root.confirmed


    @staticmethod
    def resolve_expired(root: Any, info: graphene.ResolveInfo) -> graphene.Boolean:
        return root.expired


    @staticmethod
    def resolve_client(root: Any, info: graphene.ResolveInfo) -> graphene.String:
        return info.context.loaders.client.load(root.client_id)


    @staticmethod
    def resolve_provider(root: Any, info: graphene.ResolveInfo) -> graphene.String:

        appointment = info.context.loaders.appointment.load(root.appointment_id)
        provider = appointment.then(lambda res: info.context.loaders.provider.load(res.provider_id))

        return provider


    @classmethod
    def is_type_of(cls, root: Any, info: graphene.ResolveInfo) -> bool:
        return isinstance(root, Reservation)


    @classmethod
    def get_node(cls, info: graphene.ResolveInfo, decoded_id: str) -> Promise[Optional[Any]]:
        key = int(decoded_id)
        return info.context.loaders.reservation.load(key)


class ReservationConnection(graphene.Connection):

    class Meta:
        node = ReservationType


class Query(graphene.ObjectType):

    reservation = graphene.Node.Field(ReservationType)
    reservations = graphene.ConnectionField(ReservationConnection)

    active_reservations = graphene.ConnectionField(ReservationConnection)
    confirmed_appointments = graphene.ConnectionField(ReservationConnection)
    expired_appointments = graphene.ConnectionField(ReservationConnection)


    @staticmethod
    def resolve_reservations(root: None, info: graphene.ResolveInfo, **kwargs) -> Iterable[Any]:
        return Reservation.objects.all()


    @staticmethod
    def resolve_active_reservations(root: None, info: graphene.ResolveInfo, **kwargs) -> Iterable[Any]:
        return Reservation.active_objects.all()


    @staticmethod
    def resolve_confirmed_reservations(root: None, info: graphene.ResolveInfo, **kwargs) -> Iterable[Any]:
        return Reservation.confirmed_objects.all()


    @staticmethod
    def resolve_expired_reservations(root: None, info: graphene.ResolveInfo, **kwargs) -> Iterable[Any]:
        return Reservation.expired_objects.all()
