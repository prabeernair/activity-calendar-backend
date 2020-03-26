# backend
The server-side application.

## How does it look like?
{TBD: API examples}

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
* packaging and deps management: [`poetry`](https://poetry.eustace.io/docs/basic-usage/)
* linter: [`pycodestyle`](https://pycodestyle.readthedocs.io/en/latest/)
* unit tests: [`pytest`](https://pytest.org/en/latest/)

### deps
* framework: [`pyramid`](https://docs.pylonsproject.org/projects/pyramid/en/1.10-branch/)
* DB: [PostgreSQL](https://www.postgresql.org/docs/12/index.html), possibly in a [Docker](https://docs.docker.com/) container (also consider [`podman`](https://podman.io/) + [`buildah`](https://buildah.io/))

## Development setup
```bash
# TBD: env, deps, linter, tests, build, deploy
```
