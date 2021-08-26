# backend
Server-side things: DB, scripts. Potentially to become an API for "activity-calendar" frontend.

## How does it look like?
### Import activities from JSON file to DB
```bash
$ poetry run python ./src/scripts/json-import.py 1 ../app-frontend/data/activities.json
```

## How to run it?
{TBD: links to testing/staging app instances}

## Design
### Authentication
Magic links (with or without email) instead of email + password.
Currently each link is a UUID (forever valid), should be switched to JWT.

### Data conversion (DB -> API)
* `user.id` field is not exposed, profiles are identified by `user.public_id`
* all `<...>_at` fields are exposed only to admin users
* `activity.duration` (`TSRANGE`) field is split into `data` (`YYYY-MM-DD HH:MM`) + `duration` (`H:MM:SS`) properties
* `activity.fields` (`JSONB`) field is extracted into arbitrary properties (e.g. `distance`, `surface`)

## What makes it possible?
### dev deps
* python versioning: [`pyenv`](https://github.com/pyenv/pyenv/)
* packaging and deps management: [`poetry`](https://python-poetry.org/docs/basic-usage/)
* linter: [`pycodestyle`](https://pycodestyle.readthedocs.io/en/latest/)
* unit tests: [`pytest`](https://pytest.org/en/latest/)

### deps
* SQL toolkit: [`sqlalchemy`](https://www.sqlalchemy.org/)
* DB: [PostgreSQL](https://www.postgresql.org/docs/12/index.html)

### deps to consider:
* scripting:
  * HTTP transport: [`requests`](https://github.com/psf/requests)
* app framework:
  * [`pyramid`](https://docs.pylonsproject.org/projects/pyramid/en/latest/)
  * [`fastapi`](https://github.com/tiangolo/fastapi)
* container:
  * [Docker](https://docs.docker.com/)
  * [`podman`](https://podman.io/) + [`buildah`](https://buildah.io/)

## Development setup
### Postgres
```bash
$ brew install postgres
$ brew services start postgresql
# $ psql postgres

$ createdb activity_calendar
$ psql activity_calendar < db/schema.sql
# $ pg_dump activity_calendar > db/dump.sql
# $ psql --set ON_ERROR_STOP=on activity_calendar < db/dump.sql
```

### Python
```bash
# python version
$ brew install pyenv
# $ pyenv install --list
$ pyenv install 3.8.2
# $ pyenv local 3.8.2
# $ pyenv shell 3.8.2

# env/deps
$ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
$ poetry install
# $ poetry update

# linting
$ poetry run pycodestyle --show-source ./src/

# unit tests
$ poetry run pytest ./src/
```
