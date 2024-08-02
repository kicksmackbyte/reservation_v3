from .appointment import Mutation as AppointmentMutation
from .client import Mutation as ClientMutation
from .provider import Mutation as ProviderMutation
from .reservation import Mutation as ReservationMutation


class Mutation(
    AppointmentMutation,
    ClientMutation,
    ProviderMutation,
    ReservationMutation,
):
    pass
