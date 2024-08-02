# Setup
## Dependencies
* docker compose (required)
    - tested with latest v2.29.1 release
* postman (optional)

## Running
1. `docker-compose up`
2. server will be running at http://localhost/graphql
    - can run introspection query on postman to explore schema

* See [Examples](examples/README.md)

# Repo Overview
## top-level
* `compose.yml`
    - for `docker-compose`
    - lists django service for application + nginx for reverse proxy
* `manage.py`
    - used to run dev server, database migrations, tests, etc.
* `Pipfile` + `Pipfile.lock`
    - used by `pipenv` to install dependencies + manage virtualenv
* [api](api/README.md)
    - graphQL specific code
* [devops](devops/README.md)
    - Dockerfile(s)
* [reservation](reservation/README.md)
    - data model
* [settings](settings/README.md)

# Limitations
* Django [ORM is synchronous](https://docs.djangoproject.com/en/5.0/topics/async/#asynchronous-support)
* gunicorn recommends [(2 x $numcores) + 1 worker threads](https://docs.gunicorn.org/en/latest/design.html#how-many-workers)
* Would keep an eye on the above and determine if horizontal scaling is appropriate based on access patterns or if better to migrate to a more performant stack

# TODO
## QOL features
* add common filters + sorting to API

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
    - stage gates
* load balancer
    - rolling deployments
* stand up postgreSQL server

## Developer experience
* documentation
* branch protection
* githooks to run static analysis, tests, etc.
* continue adding type hints
* diagrams
