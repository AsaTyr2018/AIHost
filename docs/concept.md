# AIHost Project Concept

AIHost provides a small web interface to manage machine learning
applications defined through Docker Compose. Each application lives in a
subdirectory under `compose/` that contains a `docker-compose.yml`
file. The folder name becomes the application identifier.

Docker images are built outside of AIHost and published to a registry.
AIHost does not clone repositories or build images locally. Instead the
web interface exposes controls to run `docker compose` commands in the
corresponding application folder.

## Core Features

1. **Application Detection**
   - At startup the backend scans the `compose/` directory for
     subfolders containing a `docker-compose.yml`.
   - The detected folders are presented in the UI as available
     applications.

2. **Application Management**
   - Users can start, stop, rebuild or remove an application. These
     actions simply invoke `docker compose` within the application's
     folder.
   - Container status and exposed ports are retrieved from the Docker
     daemon and displayed on the dashboard.

3. **Web Interface**
   - Implemented with Flask and styled using a dark theme.
   - Shows CPU and memory usage alongside the list of containers and
     available applications.

## Directory Layout

- `src/` – Web server and service logic.
- `compose/` – One subdirectory per application containing a
  `docker-compose.yml` and optional persistent data.
- `docs/` – Project documentation.

