# mutation
## AppointmentBulkCreate
* See [appointment.py](appointment.py#29)
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

## ClientCreate
* See [client.py](client.py#24)
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

## ProviderCreate
* See [provider.py](provider.py#24)
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

## ReservationCreate
* See [reservation.py](reservation.py#26)
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

## ReservationConfirm
* See [reservation.py](reservation.py#58)
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
