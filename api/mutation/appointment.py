import graphene
import datetime
from datetime import timezone

from api.utils import from_global_id

from reservation.models import Appointment, Provider

#TODO: timeslot length
TIME_SLOT_LENGTH = 15


class AppointmentBulkCreateInput(graphene.InputObjectType):

    provider_id = graphene.ID(required=True)

    start_time = graphene.DateTime(required=True)
    end_time = graphene.DateTime(required=True)


class AppointmentBulkCreate(graphene.Mutation):

    class Arguments:

        input_ = graphene.Argument(AppointmentBulkCreateInput, name='input', required=True)

    appointments = graphene.ConnectionField('api.query.appointment.AppointmentConnection')


    @classmethod
    def mutate(cls, root, info, input_):

        provider_id = input_.pop('provider_id')
        decoded_provider_id = int(from_global_id(provider_id).type_id)
        provider = Provider.objects.get(id=decoded_provider_id)

        start_time = input_.pop('start_time')
        end_time = input_.pop('end_time')

        delta = end_time - start_time
        minutes = int(delta.total_seconds()) // 60
        num_time_slots = minutes // TIME_SLOT_LENGTH

        appointment_data = []

        for slot_num in range(num_time_slots):

            offset = slot_num * TIME_SLOT_LENGTH
            time_slot = start_time + datetime.timedelta(minutes=offset)
            time_slot = time_slot.replace(tzinfo=timezone.utc)

            appointment = Appointment(time_slot=time_slot, provider=provider)
            appointment_data.append(appointment)


        appointments = Appointment.objects.bulk_create(appointment_data)
        return cls(appointments=appointments)


class Mutation(graphene.ObjectType):
    appointment_bulk_create = AppointmentBulkCreate.Field()
