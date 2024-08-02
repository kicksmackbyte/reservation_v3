# loaders
* [utils.py](utils.py)
    - holds a multitude of helper functions to wrap around `promise.dataloader`
    - of note are:
        * `batch_load_primary_key`
            - given a Model + list of primary keys, make a batched request to the ORM and map a single record back to given PK
        * `batch_load_foreign_key`
            - given a Model + list of foreign keys, make a batched request to the ORM and map a list of records back to given FK

# example
```
class ReservationLoaders:

    @cached_property
    def reservation(self) -> DataLoader:
        reservation_load_fn = batch_load_primary_key('reservation', 'Reservation')
        return DataLoader(reservation_load_fn)


    @cached_property
    def reservations_from_client(self) -> DataLoader:
        reservation_load_fn = batch_load_foreign_key('reservation', 'Reservation', 'client')
        return DataLoader(reservation_load_fn)


    @cached_property
    def active_reservations_from_client(self) -> DataLoader:
        reservation_load_fn = batch_load_foreign_key('reservation', 'Reservation', 'client', manager_name='active_objects')
        return DataLoader(reservation_load_fn)
```

## ReservationLoaders.reservation
Given a primary key, return the [Reservation record](../../reservation/models/reservation.py) associated with that PK
Batches a call to `Reservation.objects.filter(id__in=[key1, key2, key3])`


## ReservationLoaders.reservations_from_client
Given a foreign key (i.e. - Reservation.client_id), return the list of [Reservation records](../../reservation/models/reservation.py) associated with that FK
Batches a call to `Reservation.objects.filter(client_id__in=[key1, key2, key3])`


## ReservationLoaders.active_reservations_from_client
Given a foreign key (i.e. - Reservation.client_id), return the list of [Active Reservation records](../../reservation/models/reservation.py) associated with that FK
Batches a call to `Reservation.active_objects.filter(client_id__in=[key1, key2, key3])`
Makes use of custom model managers for ease of use and to add commonly used filter conditions
