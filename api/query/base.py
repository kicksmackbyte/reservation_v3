from .appointment import Query as AppointmentQuery
from .client import Query as ClientQuery
from .provider import Query as ProviderQuery
from .reservation import Query as ReservationQuery


class Query(
    AppointmentQuery,
    ClientQuery,
    ProviderQuery,
    ReservationQuery,
):
    pass
