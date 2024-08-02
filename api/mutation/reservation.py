import graphene
from graphql import GraphQLError


from api.utils import from_global_id

from reservation.models import Appointment, Client, Reservation


class ReservationCreateInput(graphene.InputObjectType):

    client_id = graphene.ID(required=True)
    appointment_id = graphene.ID(required=True)


class ReservationCreate(graphene.Mutation):

    class Arguments:

        input_ = graphene.Argument(ReservationCreateInput, name='input', required=True)

    reservation = graphene.Field('api.query.reservation.ReservationType')


    @classmethod
    def mutate(cls, root, info, input_):

        client_id = input_.pop('client_id')
        decoded_client_id = int(from_global_id(client_id).type_id)
        client = Client.objects.get(id=decoded_client_id)

        appointment_id = input_.pop('appointment_id')
        decoded_appointment_id = int(from_global_id(appointment_id).type_id)

        #NOTE: Throws error if appointment is not available
        #TODO: Race condition
        appointment = Appointment.available_objects.get(id=decoded_appointment_id)

        reservation = Reservation.objects.create(client=client, appointment=appointment)
        return cls(reservation=reservation)


class ReservationConfirmInput(graphene.InputObjectType):

    reservation_id = graphene.ID(required=True)


class ReservationConfirm(graphene.Mutation):

    class Arguments:

        input_ = graphene.Argument(ReservationConfirmInput, name='input', required=True)

    reservation = graphene.Field('api.query.reservation.ReservationType')


    @classmethod
    def mutate(cls, root, info, input_):

        reservation_id = input_.pop('reservation_id')
        decoded_reservation_id = int(from_global_id(reservation_id).type_id)
        reservation = Reservation.objects.get(id=decoded_reservation_id)

        #TODO: Attach JWT with user_id to verify they own this reservation

        if reservation.expired:
            raise GraphQLError('Reservation has expired.')

        reservation.confirmed = True
        reservation.save(update_fields=['confirmed'])

        return cls(reservation=reservation)


class Mutation(graphene.ObjectType):
    reservation_create = ReservationCreate.Field()
    reservation_confirm = ReservationConfirm.Field()
