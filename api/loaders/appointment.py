from django.utils.functional import cached_property

from .utils import batch_load_primary_key, batch_load_many_to_many_key, DataLoader


class AppointmentLoaders:

    @cached_property
    def appointment(self) -> DataLoader:
        appointment_load_fn = batch_load_primary_key('reservation', 'Appointment')
        return DataLoader(appointment_load_fn)


    #TODO: Use object managers for reserved/confirmed/available
    @cached_property
    def client_reserved_appointments(self) -> DataLoader:
        appointment_load_fn = batch_load_many_to_many_key('reservation', 'Reservation', 'client', 'appointment_id')
        return DataLoader(appointment_load_fn)


    @cached_property
    def client_confirmed_appointments(self) -> DataLoader:
        appointment_load_fn = batch_load_many_to_many_key('reservation', 'Reservation', 'client', 'appointment_id')
        return DataLoader(appointment_load_fn)


    @cached_property
    def provider_available_appointments(self) -> DataLoader:
        appointment_load_fn = batch_load_many_to_many_key('reservation', 'Reservation', 'appointment__provider', 'appointment_id')
        return DataLoader(appointment_load_fn)


    @cached_property
    def provider_reserved_appointments(self) -> DataLoader:
        appointment_load_fn = batch_load_many_to_many_key('reservation', 'Reservation', 'appointment__provider', 'appointment_id')
        return DataLoader(appointment_load_fn)


    @cached_property
    def provider_confirmed_appointments(self) -> DataLoader:
        appointment_load_fn = batch_load_many_to_many_key('reservation', 'Reservation', 'appointment__provider', 'appointment_id')
        return DataLoader(appointment_load_fn)


    @cached_property
    def provider_schedule(self) -> DataLoader:
        appointment_load_fn = batch_load_many_to_many_key('reservation', 'Reservation', 'appointment__provider', 'appointment_id')
        return DataLoader(appointment_load_fn)
