from django.utils.functional import cached_property

from .utils import batch_load_primary_key, DataLoader


class ModelLoaders:

    @cached_property
    def model(self) -> DataLoader:
        model_load_fn = batch_load_primary_key('reservation', 'Model')
        return DataLoader(model_load_fn)

