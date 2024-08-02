from django.utils.functional import cached_property

from .utils import batch_load_primary_key, batch_load_foreign_key, batch_load_many_to_many_key, DataLoader


class ReservationLoaders:

    @cached_property
    def reservation(self) -> DataLoader:
        reservation_load_fn = batch_load_primary_key('reservation', 'Reservation')
        return DataLoader(reservation_load_fn)


    @cached_property
    def reservations_from_appointment(self) -> DataLoader:
        reservation_load_fn = batch_load_foreign_key('reservation', 'Reservation', 'appointment')
        return DataLoader(reservation_load_fn)


    @cached_property
    def reservations_from_client(self) -> DataLoader:
        reservation_load_fn = batch_load_foreign_key('reservation', 'Reservation', 'client')
        return DataLoader(reservation_load_fn)


    @cached_property
    def active_reservations_from_client(self) -> DataLoader:
        reservation_load_fn = batch_load_foreign_key('reservation', 'Reservation', 'client', manager_name='active_objects')
        return DataLoader(reservation_load_fn)


    @cached_property
    def confirmed_reservations_from_client(self) -> DataLoader:
        reservation_load_fn = batch_load_foreign_key('reservation', 'Reservation', 'client', manager_name='confirmed_objects')
        return DataLoader(reservation_load_fn)


    @cached_property
    def expired_reservations_from_client(self) -> DataLoader:
        reservation_load_fn = batch_load_foreign_key('reservation', 'Reservation', 'client', manager_name='expired_objects')
        return DataLoader(reservation_load_fn)
