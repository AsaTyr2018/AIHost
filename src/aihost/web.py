from __future__ import annotations

from flask import Flask, render_template, request, redirect, url_for
import psutil

from .container_manager import (
    list_containers,
    list_apps,
    start_app,
    stop_app,
    rebuild_app,
    remove_app,
)

app = Flask(__name__)


@app.route("/")
def dashboard():
    cpu_percent = psutil.cpu_percent()
    mem_percent = psutil.virtual_memory().percent
    containers = list_containers()
    apps = list_apps()
    total_containers = len(containers)
    running = sum(1 for c in containers if c.ports)
    return render_template(
        "dashboard.html",
        cpu_percent=cpu_percent,
        mem_percent=mem_percent,
        containers=containers,
        apps=apps,
        total_containers=total_containers,
        running=running,
    )


@app.route("/apps", methods=["POST"])
def apps_action():
    name = request.form["name"]
    action = request.form["action"]
    if action == "start":
        start_app(name)
    elif action == "stop":
        stop_app(name)
    elif action == "rebuild":
        rebuild_app(name)
    elif action == "remove":
        remove_app(name)
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
