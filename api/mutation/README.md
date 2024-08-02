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
```

## ProviderCreate
* See [provider.py](provider.py#24)
```
```

## ReservationCreate
* See [reservation.py](reservation.py#26)
```
```

## ReservationConfirm
* See [reservation.py](reservation.py#58)
```
```
