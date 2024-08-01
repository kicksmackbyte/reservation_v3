from django.utils.functional import cached_property

from .utils import batch_load_primary_key, DataLoader


class ClientLoaders:

    @cached_property
    def client(self) -> DataLoader:
        client_load_fn = batch_load_primary_key('reservation', 'Client')
        return DataLoader(client_load_fn)

