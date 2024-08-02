from .client import Mutation as ClientMutation
from .provider import Mutation as ProviderMutation


class Mutation(
    ClientMutation,
    ProviderMutation,
):
    pass
