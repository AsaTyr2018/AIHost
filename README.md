# AIHost

AIHost aims to be a simple, automated Docker manager for running
machine‑learning projects. Repositories are registered via a web
interface, installed on demand and executed inside containers built from
a default AI‑ready base image.

The high level design is described in [docs/concept.md](docs/concept.md).
See `AGENTS.md` for coding conventions and project structure.

The project includes a minimal container manager able to discover
containers on the local Docker host. The manager lists container names
along with exposed ports as clickable links and provides start, stop,
rebuild and remove actions.

A small Flask based web interface exposes these features. The dashboard
shows CPU and memory usage, counts running containers and links to their
exposed ports. A repository registry allows adding or deleting
repositories while the container view offers start, stop, rebuild and
remove controls.

## Installation and Usage

Run `scripts/install.sh` to install AIHost into `/opt/AIHost` (or a custom path). The installer creates a Python virtual environment, installs dependencies and optionally registers a `systemd` service.

Start the application with `scripts/start.sh`. The starter checks the repository for updates before launching the web server.

To update an existing installation run `scripts/update.sh`. It performs `git pull`, installs new dependencies if needed and restarts the service when installed.
