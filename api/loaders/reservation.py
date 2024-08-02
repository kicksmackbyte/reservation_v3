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
