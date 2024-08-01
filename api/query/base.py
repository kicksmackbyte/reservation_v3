from .client import Query as ClientQuery
from .provider import Query as ProviderQuery


class Query(
    ClientQuery,
    ProviderQuery,
):
    pass
