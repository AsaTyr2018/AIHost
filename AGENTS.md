# AIHost Agent Guidelines

This repository defines an example project called **AIHost**. Contributors
should follow these conventions when modifying or adding code.

## Directory Structure

- `src/` contains the Python sources for the web interface and service
  logic. Use packages under `src/aihost/`.
- `data/` holds runtime data such as cloned repositories or persistent
  volumes. It should not be tracked by git.
- `compose/` contains one subdirectory per application. Each subdirectory
  includes a `docker-compose.yml` used to run that application.
- `docs/` stores design and concept documentation.

## Application Detection

AIHost scans the `compose/` directory for subfolders containing a
`docker-compose.yml`. The name of each subfolder is treated as the
application identifier. The backend uses these files when running Docker
Compose commands and no manual repository registration is required.

## Coding Standards

- Write code in **Python 3.10+** using type hints.
- Run `black` for code formatting and `flake8` for linting before
  committing.
- Tests are executed with `pytest`. If you add or modify functionality,
  include corresponding unit tests under `tests/`.

## Commit Guidelines

- Keep commits focused on a single change and include a clear commit
  message.
- After making changes run `pytest` and linting checks. The commit
  should not break existing tests.

## Documentation

Update `docs/` and `README.md` whenever behaviour or features change.
Keep documentation concise and in Markdown format.

