from .appointment import Query as AppointmentQuery
from .client import Query as ClientQuery
from .provider import Query as ProviderQuery


class Query(
    AppointmentQuery,
    ClientQuery,
    ProviderQuery,
):
    pass
