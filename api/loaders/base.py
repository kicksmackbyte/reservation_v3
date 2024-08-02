from .appointment import AppointmentLoaders
from .client import ClientLoaders
from .provider import ProviderLoaders

class Loaders(
    AppointmentLoaders,
    ClientLoaders,
    ProviderLoaders,
):
    pass
