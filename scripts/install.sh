#!/usr/bin/env bash
set -e

REPO_URL="https://github.com/AsaTyr2018/AIHost"
APP_DIR="/opt/AIHost"
SERVICE_FILE="/etc/systemd/system/aihost.service"

print_header() {
    printf '\n\033[1;35m%s\033[0m\n' "============================="
    printf '\033[1;35m%s\033[0m\n' "    AIHost Installer"
    printf '\033[1;35m%s\033[0m\n\n' "============================="
}

print_header
read -p "Install path [${APP_DIR}]: " input_dir
APP_DIR=${input_dir:-$APP_DIR}
read -p "Repository URL [${REPO_URL}]: " input_repo
REPO_URL=${input_repo:-$REPO_URL}

# Check and install required apt packages
check_apt_package() {
    local pkg=$1
    if ! dpkg -s "$pkg" >/dev/null 2>&1; then
        printf '\033[1;34mInstalling %s...\033[0m\n' "$pkg"
        sudo apt-get update
        sudo apt-get install -y "$pkg"
    fi
}

ensure_system_dependencies() {
    if command -v apt-get >/dev/null 2>&1; then
        local ver
        ver=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
        check_apt_package "python${ver}-venv"
    fi
}

ensure_system_dependencies

# Ensure the repository URL uses HTTPS in case a git@ or ssh URL was provided
convert_to_https() {
    local url=$1
    if [[ $url =~ ^git@([^:]+):(.+)$ ]]; then
        printf "https://%s/%s" "${BASH_REMATCH[1]}" "${BASH_REMATCH[2]}"
    elif [[ $url =~ ^ssh://git@([^/]+)/(.+)$ ]]; then
        printf "https://%s/%s" "${BASH_REMATCH[1]}" "${BASH_REMATCH[2]}"
    else
        printf "%s" "$url"
    fi
}

# Convert possible SSH style repo URLs to HTTPS
REPO_URL=$(convert_to_https "$REPO_URL")

printf '\033[1;34mCloning repository...\033[0m\n'
mkdir -p "$APP_DIR"
if [ -d "$APP_DIR/.git" ]; then
    echo "Directory already contains a git repository. Skipping clone."
else
    git clone "$REPO_URL" "$APP_DIR"
fi

printf '\033[1;34mSetting up virtual environment...\033[0m\n'
python3 -m venv "$APP_DIR/venv"
source "$APP_DIR/venv/bin/activate"

if [ -f "$APP_DIR/requirements.txt" ]; then
    printf '\033[1;34mInstalling requirements...\033[0m\n'
    pip install -r "$APP_DIR/requirements.txt"
fi

deactivate

read -p "Install systemd service for auto start? [y/N]: " yn
if [[ $yn =~ ^[Yy]$ ]]; then
    printf '\033[1;34mCreating service file...\033[0m\n'
    sudo tee "$SERVICE_FILE" >/dev/null <<SERVICE
[Unit]
Description=AIHost Service
After=network.target docker.service

[Service]
Type=simple
WorkingDirectory=${APP_DIR}
ExecStart=${APP_DIR}/venv/bin/python -m aihost.web
Environment=PYTHONPATH=${APP_DIR}/src
Restart=on-failure

[Install]
WantedBy=multi-user.target
SERVICE
    sudo systemctl daemon-reload
    sudo systemctl enable aihost.service
    echo "Service installed as aihost.service"
fi

printf '\n\033[1;32mInstallation complete!\033[0m\n'
