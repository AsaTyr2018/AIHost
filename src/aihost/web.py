from __future__ import annotations

from flask import Flask, render_template, request, redirect, url_for
import psutil

from .container_manager import (
    list_containers,
    start_container,
    stop_container,
    rebuild_container,
    remove_container,
)
from .registry import list_repos, add_repo, delete_repo


app = Flask(__name__)


@app.route("/")
def dashboard():
    cpu_percent = psutil.cpu_percent()
    mem_percent = psutil.virtual_memory().percent
    containers = list_containers()
    total_containers = len(containers)
    running = sum(1 for c in containers if c.ports)
    return render_template(
        "dashboard.html",
        cpu_percent=cpu_percent,
        mem_percent=mem_percent,
        containers=containers,
        total_containers=total_containers,
        running=running,
    )


@app.route("/repos", methods=["GET", "POST"])
def repos():
    if request.method == "POST":
        if "delete" in request.form:
            delete_repo(request.form["delete"])
        else:
            add_repo(
                request.form["name"],
                request.form["url"],
                request.form["start_command"],
            )
        return redirect(url_for("repos"))
    return render_template("repos.html", repos=list_repos())


@app.route("/containers", methods=["POST"])
def containers_action():
    name = request.form["name"]
    action = request.form["action"]
    if action == "start":
        start_container(name)
    elif action == "stop":
        stop_container(name)
    elif action == "rebuild":
        rebuild_container(name, path=".")
    elif action == "remove":
        remove_container(name)
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True)
