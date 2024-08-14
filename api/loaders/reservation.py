from collections import defaultdict

from django.utils.functional import cached_property
from django.db.models import F

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
    def reservations_from_provider(self) -> DataLoader:

        def batch_load_reservations_from_provider():

            def batch_load_fn(model_ids):
                from reservation.models import Reservation

                reservations = Reservation.objects.filter(appointment__provider_id__in=model_ids).annotate(provider_id=F('appointment__provider_id'))
                model_map = defaultdict(list)

                for reservation in reservations:
                    provider_id = getattr(reservation, f'provider_id')
                    model_map[provider_id].append(reservation)

                return [model_map.get(model_id, []) for model_id in model_ids]
            return batch_load_fn

        reservation_load_fn = batch_load_reservations_from_provider()
        return DataLoader(reservation_load_fn)


    @cached_property
    def expired_reservations_from_client(self) -> DataLoader:
        reservation_load_fn = batch_load_foreign_key('reservation', 'Reservation', 'client', manager_name='expired_objects')
        return DataLoader(reservation_load_fn)
