from __future__ import annotations

from flask import Flask, render_template, request, redirect, url_for
import psutil

from .gpu import get_gpu_stats

from .container_manager import (
    list_containers,
    list_apps,
    start_container,
    stop_container,
    rebuild_container,
    install_app,
    deinstall_app,
)

app = Flask(__name__)


@app.route("/")
def dashboard():
    active_tab = request.args.get("tab", "containers")
    cpu_percent = psutil.cpu_percent()
    mem_percent = psutil.virtual_memory().percent
    gpu = get_gpu_stats()
    containers = list_containers()
    apps = list_apps()
    total_containers = len(containers)
    running = sum(1 for c in containers if c.ports)
    return render_template(
        "dashboard.html",
        cpu_percent=cpu_percent,
        mem_percent=mem_percent,
        gpu=gpu,
        containers=containers,
        apps=apps,
        total_containers=total_containers,
        running=running,
        active_tab=active_tab,
    )


@app.route("/containers", methods=["POST"])
def containers_action():
    name = request.form["name"]
    action = request.form["action"]
    if action == "start":
        start_container(name)
    elif action == "stop":
        stop_container(name)
    elif action == "rebuild":
        rebuild_container(name)
    return redirect(url_for("dashboard"))


@app.route("/apps", methods=["POST"])
def apps_action():
    name = request.form["name"]
    action = request.form["action"]
    if action == "install":
        install_app(name)
    elif action == "deinstall":
        deinstall_app(name)
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
