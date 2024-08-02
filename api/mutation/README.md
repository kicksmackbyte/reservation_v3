# mutation
* Limitations presented here should be captured as test cases to explicitly define specification

## AppointmentBulkCreate
```
mutation AppointmentBulkCreate($input:AppointmentBulkCreateInput!) {
  appointmentBulkCreate(input: $input) {
    appointments {
      edges {
        node {
          id
          timeSlot
          provider {
            id
            firstName
            lastName
          }
        }
      }
    }
  }
}
```
* See [appointment.py](appointment.py#29)
* Limitations
    - Should attach JWT + verify provider role + id and user provider_id in token
    - Should handle provider "double-booking" overlapping time ranges
        * Should the system throw an error?
        * Should the system gracefully expand the pre-existing appointment slots to include new range (if any)?
        * Should the system allow multiple appointments within the same timeslot? This could allow for an information session with multiple seats.
    - Should perform validations on `start_time` + `end_time`
        * `start_time` should come before `end_time`
        * `start_time - end_time` should be in 15-min chunks
    - Consider separate mutation for a recurring schedule

## ClientCreate
```
mutation ClientCreate($input: ClientCreateInput!) {
  clientCreate(input: $input) {
    client {
      id
      firstName
      lastName
    }
  }
}
```
* See [client.py](client.py#24)
* Limitations
    - Consider single user table with multiple roles

## ProviderCreate
```
mutation ProviderCreate($input: ProviderCreateInput!) {
  providerCreate(input: $input) {
    provider {
      id
      firstName
      lastName
    }
  }
}
```
* See [provider.py](provider.py#24)
* Limitations
    - Consider single user table with multiple roles

## ReservationCreate
```
mutation ReservationCreate($input: ReservationCreateInput!) {
  reservationCreate(input: $input) {
    reservation {
      id
      expiry
      expired
      confirmed
      client {
        id
        firstName
        lastName
      }
      provider {
        id
        firstName
        lastName
      }
      appointment {
        id
        timeSlot
      }
    }
  }
}
```
* See [reservation.py](reservation.py#26)
* Limitations
    - Should throw a more informative error if given appointment is not available
    - Should check client is not double booked at the same timeslot
    - Should handle race condition when two requests for the same timeslot come in and we reach the [cricital section](reservation.py#37)

## ReservationConfirm
```
mutation ReservationConfirm($input: ReservationConfirmInput!) {
  reservationConfirm(input: $input) {
    reservation {
      id
      expiry
      expired
      confirmed
      client {
        id
        firstName
        lastName
      }
      provider {
        id
        firstName
        lastName
      }
      appointment {
        id
        timeSlot
      }
    }
  }
}
```
* See [reservation.py](reservation.py#58)
* Limitations
    - Should attach JWT + verify client role + id and validate reservation matches client id
