import graphene

from api.utils import from_global_id

from reservation.models import Appointment, Client, Reservation


class ReservationCreateInput(graphene.InputObjectType):

    client_id = graphene.ID(required=True)
    appointment_id = graphene.ID(required=True)


class ReservationCreate(graphene.Mutation):

    class Arguments:

        input_ = graphene.Argument(ReservationCreateInput, name='input', required=True)

    client = graphene.Field('api.query.client.ClientType')
    appointment = graphene.Field('api.query.appointment.AppointmentType')


    @classmethod
    def mutate(cls, root, info, input_):

        client_id = input_.pop('client_id')
        decoded_client_id = int(from_global_id(client_id).type_id)
        client = Client.objects.get(id=decoded_client_id)

        appointment_id = input_.pop('appointment_id')
        decoded_appointment_id = int(from_global_id(appointment_id).type_id)
        appointment = Appointment.available_objects.get(id=decoded_appointment_id)

        reservation = Reservation.objects.create(client=client, appointment=appointment)
        return cls(client=client, appointment=appointment)


class Mutation(graphene.ObjectType):
    reservation_create = ReservationCreate.Field()
