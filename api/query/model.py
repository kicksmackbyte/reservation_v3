from typing import Any, Iterable, List, Optional

import graphene
from promise import Promise
from reservation.models import Model


class ModelType(graphene.ObjectType):

    class Meta:
        interfaces = (graphene.Node, )

    name = graphene.String()


    @staticmethod
    def resolve_name(root: Any, info: graphene.ResolveInfo) -> graphene.String:
        return "Alberto"


    @classmethod
    def is_type_of(cls, root: Any, info: graphene.ResolveInfo) -> bool:
        return isinstance(root, Model)


    @classmethod
    def get_node(cls, info: graphene.ResolveInfo, decoded_id: str) -> Promise[Optional[Any]]:
        key = int(decoded_id)
        return info.context.loaders.model.load(key)


class ModelConnection(graphene.Connection):

    class Meta:
        node = ModelType


class Query(graphene.ObjectType):

    model = graphene.Node.Field(ModelType)
    models = graphene.ConnectionField(ModelConnection)


    @staticmethod
    def resolve_models(root: None, info: graphene.ResolveInfo, **kwargs) -> Iterable[Any]:
        return Model.objects.all()
