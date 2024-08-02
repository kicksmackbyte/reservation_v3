# Setup
## Dependencies
- docker compose (required)
    a. tested with latest v2.29.1 release
- postman (optional)

## Running
1. `docker-compose up`
2. server will be running at http://localhost/graphql
    - can run introspection query on postman to explore schema

# Repo Overview
## top-level
* `compose.yml`
    - for `docker-compose`
    - lists django service for application + nginx for reverse proxy
* `manage.py`
    - used to run dev server, database migrations, tests, etc.
* `Pipfile` + `Pipfile.lock`
    - used by `pipenv` to install dependencies + manage virtualenv

## api
* module that primarily holds graphene_django-specific code (i.e. - graphQL)
* `schema.py`
    - can subclass `graphene.Schema` to manipulate available queries + mutations + types
* `utils.py`
    - helper functions to go back and forth from b64encoded, global ids (for relay)
* `views.py`
    - attaches context to request for use in all resolvers (i.e. - `info.context`)
    - good place to attach JWT to request for resolvers to validate permissions
### loaders
* DataLoader for graphQL resolvers to make use of instead of going directly through ORM

### mutation
* `appointment.py`
* `client.py`
* `provider.py`
* `reservation.py`

### query
* `appointment.py`
* `client.py`
* `provider.py`
* `reservation.py`
## devops
## reservation
* module that primarily holds django-specific code
* `urls.py`
    - lists available routes (i.e. - /graphql/ endpoint with schema)
### migrations
* generated by `python manage.py makemigrations` command + committed to repo
* can be replaced by raw SQL or ported
### models
* `appointment.py`
* `client.py`
* `provider.py`
* `reservation.py`

## settings
* `__init__.py`
    - has default settings
* `development.py`/`local.py`/`production.py`/`production.py`
    - `DEBUG` turned on/off
    - `SILK` middleware for database + query profiling
    - `DATABASES` for different configs

# Limitations
* Django (ORM is synchronous)[https://docs.gunicorn.org/en/latest/design.html#how-many-workers]
* gunicorn recommends ((2 x $numcores) + 1 worker threads)[https://docs.gunicorn.org/en/latest/design.html#how-many-workers]
* Would keep an eye on the above and determine if horizontal scaling is appropriate based on access patterns or if better to migrate to a more performant stack

# TODO

## Testing
* test data model
* test mutations
* test queries on frozen data + store snapshots for regression

## Security
* Identity provider + Role-based access control
* Rate limiting
* Depth limiting
* Persisted queries
* Host dependencies in private registry
* HTTPS + TLS

## Monitoring
* dump logs into DataDog
* disk + CPU alerts
* performance percentiles

## Deployment
* CI/CD with GCP Cloud Build
* load balancer
* stand up postgreSQL server

## Developer experience
* documentation
* branch protection
* githooks to run static analysis, tests, etc.
* continue adding type hints
