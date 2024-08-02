# API
* module that primarily holds graphene_django-specific code (i.e. - graphQL)
* `schema.py`
    - can subclass `graphene.Schema` to manipulate available queries + mutations + types
* `utils.py`
    - helper functions to go back and forth from b64encoded, global ids (for relay)
* `views.py`
    - attaches context to request for use in all resolvers (i.e. - `info.context`)
    - good place to attach JWT to request for resolvers to validate permissions
