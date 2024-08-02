# query

## Clients
```
query Clients {
  clients {
    edges {
      node {
        id
        firstName
        lastName
        reservations {
          edges {
            node {
              id
              expiry
              expired
              confirmed
              appointment {
                id
                timeSlot
              }
              provider {
                id
                firstName
                lastName
              }
            }
          }
        }
        activeReservations {
          edges {
            node {
              id
              appointment {
                id
                timeSlot
              }
              provider {
                id
                firstName
                lastName
              }
            }
          }
        }
        confirmedReservations {
          edges {
            node {
              id
              appointment {
                id
                timeSlot
              }
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
  }
}
```

## Providers
```
query Providers{
  providers {
    edges {
      node {
        id
        firstName
        lastName
        availableAppointments {
          edges {
            node {
              id
              timeSlot
            }
          }
        }
        confirmedAppointments {
          edges {
            node {
              id
              timeSlot
              reservation: confirmedReservation {
                id
                client {
                  id
                  firstName
                  lastName
                }
              }
            }
          }
        }
      }
    }
  }
}
```

## AvailableAppointments
```
query AvailableAppointments {
  availableAppointments {
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
```

## Reservations
```
query Reservations {
  reservations {
    edges {
      node {
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
}
```
