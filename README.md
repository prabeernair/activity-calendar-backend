# backend
The server-side application.

## How does it look like?
### Import activities from JSON file
```bash
$ python src/scripts/json-import.py 1 ../app-frontend/data/activities.json
```

## How to run it?
{TBD: links to testing/staging app instances}

## Design
### Authentication
Magic links (with or without email) instead of email + password.
Currently each link is a UUID (forever valid), should be switched to JWT.

### Data conversion (DB -> API)
* `user.id` field is not exposed, users are identified by `user.magic_link`
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
* framework: [`pyramid`](https://docs.pylonsproject.org/projects/pyramid/en/1.10-branch/)
* DB: [PostgreSQL](https://www.postgresql.org/docs/12/index.html), possibly in a [Docker](https://docs.docker.com/) container (also consider [`podman`](https://podman.io/) + [`buildah`](https://buildah.io/))

## Development setup
### Postgres
```bash
$ brew install postgres
$ brew services start postgresql
# see "src/db/schema.sql" for creating the DB
$ psql postgres
# $ psql activity_calendar
```

### Python
```bash
# python version
$ brew install pyenv
# $ pyenv install --list
$ pyenv install 3.8.2
$ pyenv shell 3.8.2

# env/deps
$ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
$ poetry install

# linting
$ poetry run pycodestyle --show-source ./src/

# unit tests
$ poetry run pytest ./src/
```
