from django.utils.functional import cached_property

from .utils import batch_load_primary_key, DataLoader


class ProviderLoaders:

    @cached_property
    def provider(self) -> DataLoader:
        provider_load_fn = batch_load_primary_key('reservation', 'Provider')
        return DataLoader(provider_load_fn)

