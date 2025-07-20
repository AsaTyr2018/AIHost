# AIHost Project Concept

AIHost is intended as a lightweight web-based manager for deploying
and running machine learning projects inside Docker containers. The
key idea is to register GitHub repositories, provide configuration for
starting them, and automatically build and run containers based on
those repositories.

## Core Features

1. **Repository Registration**
   - Users register a GitHub repository through the web interface.
   - They specify a friendly name, repository URL and a start command.
   - The start command is used by Docker Compose when launching the
     container.

2. **Repository Listing**
   - After registration, repositories are listed with their status:
     uninstalled, installed or running.
   - Users can install or start/stop the container from the list.

3. **Installation Process**
   - On install the system performs `git clone` into a managed
     directory.
   - If the repository contains a `requirements.txt` file, the
     container is built using a base image with GPU/AI support. This
     default base image is configurable but typically something like
     `nvidia/cuda:12.1.1-base` with Python included.
   - The install process writes a simple Dockerfile using the base
     image, copies the repo content, installs dependencies and sets the
     default command to the provided start command.

4. **Container Management**
   - Docker Compose is used to orchestrate containers. Each registered
     repository maps to a service in the main `docker-compose.yaml`.
   - Starting a container results in `docker compose up` for that
     service. Stopping uses `docker compose stop` or `down` as needed.

5. **Web Interface**
   - The web interface is minimal. It allows registration, listing and
     actions (install, start, stop, remove). Status is displayed based
     on Docker state.
   - The application is built with Flask for rapid development, but
     this can be swapped out if needed.


## Container Manager

After containers are built, AIHost detects them from the Docker host and lists them in the interface. Each listed container shows its name and any exposed ports as clickable links. Users can start, stop, rebuild or remove containers directly from the list.

## Directory Layout

- `src/` – Web server and service logic.
- `data/` – Cloned repositories live here.
- `compose/` – Generated Docker Compose and Dockerfiles.
- `docs/` – Project documentation.

## Next Steps

1. Implement the registration form and list view.
2. Implement install logic: clone repo, generate Dockerfile, add
   service entry to compose file.
3. Provide start/stop control using docker-compose.

