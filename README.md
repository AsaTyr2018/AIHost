# AIHost

AIHost acts as a lightweight Docker Compose manager for various
machine‑learning applications. Docker images are built manually outside
the system and pushed to a Docker Hub repository. Each application
stores its Compose configuration under `compose/<app>/docker-compose.yml`
along with any persistent data.

**Note:** Docker image tags must be written in lowercase to satisfy the
Docker daemon.

The high level design is described in [docs/concept.md](docs/concept.md).
See `AGENTS.md` for coding conventions and project structure.

The application automatically detects available apps by scanning the
`compose/` directory for subfolders that contain a `docker-compose.yml`
file. The folder name becomes the application name. The web interface
shows running containers with buttons to start, stop or rebuild them.
Available apps are listed in an **AppStore** tab where they can be
installed or deinstalled. Compose commands are only used for install,
deinstall and rebuild operations and
run in the respective application folder. No manual repository
registration or image building is performed by AIHost.

With images prepared ahead of time there is no in-place build step.
Compose folders serve as the central storage location for each app and
may include volume directories referenced by the compose file.

A small Flask based web interface exposes these features. The interface
uses a dark theme with rounded elements. The dashboard shows CPU and
memory usage and, when available, GPU statistics such as VRAM
utilization. It also counts running containers and links to their exposed
ports. Detected apps are presented in the AppStore with install and
deinstall controls, while running containers offer start, stop and
rebuild buttons. Each app entry also includes a **Log/Status** link that opens
the most recent container logs in a separate window.

## Installation and Usage

Run `scripts/install.sh` to install AIHost into `/opt/AIHost` (or a custom path). The installer checks for required apt packages such as `python3-venv`, creates a Python virtual environment, installs dependencies and optionally registers a `systemd` service.

Start the application with `scripts/start.sh`. The starter checks the repository for updates before launching the web server and automatically sets `PYTHONPATH` so the `aihost` package can be found. It no longer prompts for the installation path and instead uses `/opt/AIHost` by default. The web server listens on all interfaces (`0.0.0.0`) so it can be reached from other hosts.

To update an existing installation run `scripts/update.sh`. It performs `git pull`, installs new dependencies if needed and restarts the service when installed. Like the starter script, it assumes the default path `/opt/AIHost` without asking.
