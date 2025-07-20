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

The `aihost.builder` module handles installation of repositories. It
clones the specified Git repository, generates a Dockerfile based on the
CUDA image `nvidia/cuda:12.1.1-base` and builds a Docker image ready for
execution.

A small Flask based web interface exposes these features. The dashboard
shows CPU and memory usage, counts running containers and links to their
exposed ports. A repository registry allows adding or deleting
repositories while the container view offers start, stop, rebuild and
remove controls.

## Installation and Usage

Run `scripts/install.sh` to install AIHost into `/opt/AIHost` (or a custom path). The installer creates a Python virtual environment, installs dependencies and optionally registers a `systemd` service.

Start the application with `scripts/start.sh`. The starter checks the repository for updates before launching the web server and automatically sets `PYTHONPATH` so the `aihost` package can be found. It no longer prompts for the installation path and instead uses `/opt/AIHost` by default. The web server listens on all interfaces (`0.0.0.0`) so it can be reached from other hosts.

To update an existing installation run `scripts/update.sh`. It performs `git pull`, installs new dependencies if needed and restarts the service when installed. Like the starter script, it assumes the default path `/opt/AIHost` without asking.
