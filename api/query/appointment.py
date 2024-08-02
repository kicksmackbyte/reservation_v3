from typing import Any, Iterable, List, Optional

import graphene
from promise import Promise
from reservation.models import Appointment


class AppointmentType(graphene.ObjectType):

    class Meta:
        interfaces = (graphene.Node, )

    time_slot = graphene.DateTime()
    provider = graphene.Field('api.query.provider.ProviderType')

    confirmed_reservation = graphene.Field('api.query.reservation.ReservationType')
    reservations = graphene.ConnectionField('api.query.reservation.ReservationConnection')


    @staticmethod
    def resolve_time_slot(root: Any, info: graphene.ResolveInfo) -> graphene.String:
        return root.time_slot


    @staticmethod
    def resolve_provider(root: Any, info: graphene.ResolveInfo) -> graphene.String:
        return info.context.loaders.provider.load(root.provider_id)


    @staticmethod
    def resolve_confirmed_reservation(root: Any, info: graphene.ResolveInfo) -> graphene.String:

        def _unbox(res):

            confirmed_reservation = None

            if res:
                assert len(res) == 1
                confirmed_reservation = res[0]

            return confirmed_reservation


        reservations = info.context.loaders.reservations_from_appointment.load(root.id)
        confirmed_reservations = reservations.then(lambda res: [r for r in res if r.confirmed])
        confirmed_reservation = confirmed_reservations.then(lambda res: _unbox(res))

        return confirmed_reservation


    @staticmethod
    def resolve_reservations(root: Any, info: graphene.ResolveInfo) -> graphene.String:
        return info.context.loaders.reservations_from_appointment.load(root.id)


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
