from django.utils.functional import cached_property

from .utils import batch_load_primary_key, batch_load_foreign_key, batch_load_many_to_many_key, DataLoader


class AppointmentLoaders:

    @cached_property
    def appointment(self) -> DataLoader:
        appointment_load_fn = batch_load_primary_key('reservation', 'Appointment')
        return DataLoader(appointment_load_fn)


    @cached_property
    def appointments_from_provider(self) -> DataLoader:
        appointment_load_fn = batch_load_foreign_key('reservation', 'Appointment', 'provider')
        return DataLoader(appointment_load_fn)


    @cached_property
    def available_appointments_from_provider(self) -> DataLoader:
        appointment_load_fn = batch_load_foreign_key('reservation', 'Appointment', 'provider', manager_name='available_objects')
        return DataLoader(appointment_load_fn)


    @cached_property
    def confirmed_appointments_from_provider(self) -> DataLoader:
        appointment_load_fn = batch_load_foreign_key('reservation', 'Appointment', 'provider', manager_name='confirmed_objects')
        return DataLoader(appointment_load_fn)


    @cached_property
    def reserved_appointments_from_provider(self) -> DataLoader:
        appointment_load_fn = batch_load_foreign_key('reservation', 'Appointment', 'provider', manager_name='reserved_objects')
        return DataLoader(appointment_load_fn)
