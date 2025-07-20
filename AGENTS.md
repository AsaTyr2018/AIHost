# AIHost Agent Guidelines

This repository defines an example project called **AIHost**. Contributors
should follow these conventions when modifying or adding code.

## Directory Structure

- `src/` contains the Python sources for the web interface and service
  logic. Use packages under `src/aihost/`.
- `data/` is created at runtime for cloned repositories. It should not
  be tracked by git.
- `compose/` stores generated Docker Compose files and Dockerfiles.
- `docs/` stores design and concept documentation.

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

