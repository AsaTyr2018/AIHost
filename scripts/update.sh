#!/usr/bin/env bash
set -e

APP_DIR="/opt/AIHost"
SERVICE_FILE="/etc/systemd/system/aihost.service"
print_header() {
    printf '\n\033[1;36m%s\033[0m\n' "========================="
    printf '\033[1;36m%s\033[0m\n' "     AIHost Updater"
    printf '\033[1;36m%s\033[0m\n\n' "========================="
}

print_header

cd "$APP_DIR"
BRANCH=$(git rev-parse --abbrev-ref HEAD)
printf '\033[1;34mPulling latest changes...\033[0m\n'
old_rev=$(git rev-parse HEAD)
if git pull --ff-only origin "$BRANCH"; then
    new_rev=$(git rev-parse HEAD)
else
    echo "Update failed"; exit 1
fi

changed_req=$(git diff --name-only "$old_rev" "$new_rev" | grep requirements.txt || true)
if [ -n "$changed_req" ]; then
    printf '\033[1;34mRequirements changed. Installing...\033[0m\n'
    "$APP_DIR/venv/bin/pip" install -r requirements.txt
fi

if [ -f "$SERVICE_FILE" ]; then
    printf '\033[1;34mRestarting service...\033[0m\n'
    sudo systemctl restart aihost.service
fi

printf '\n\033[1;32mUpdate complete!\033[0m\n'
