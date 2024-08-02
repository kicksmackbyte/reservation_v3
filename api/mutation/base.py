from .appointment import Mutation as AppointmentMutation
from .client import Mutation as ClientMutation
from .provider import Mutation as ProviderMutation


class Mutation(
    AppointmentMutation,
    ClientMutation,
    ProviderMutation,
):
    pass
