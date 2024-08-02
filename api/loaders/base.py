from .appointment import AppointmentLoaders
from .client import ClientLoaders
from .provider import ProviderLoaders
from .reservation import ReservationLoaders

class Loaders(
    AppointmentLoaders,
    ClientLoaders,
    ProviderLoaders,
    ReservationLoaders,
):
    pass
