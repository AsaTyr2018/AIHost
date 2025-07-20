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

