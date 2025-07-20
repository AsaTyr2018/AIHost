#!/usr/bin/env bash
set -e

APP_DIR="/opt/AIHost"
print_header() {
    printf '\n\033[1;32m%s\033[0m\n' "========================="
    printf '\033[1;32m%s\033[0m\n' "    AIHost Starter"
    printf '\033[1;32m%s\033[0m\n\n' "========================="
}

print_header

cd "$APP_DIR"
BRANCH=$(git rev-parse --abbrev-ref HEAD)
printf '\033[1;34mChecking for updates...\033[0m\n'
if git fetch origin; then
    updates=$(git rev-list --count HEAD..origin/$BRANCH || echo 0)
else
    updates=0
fi

if [ "$updates" -gt 0 ]; then
    printf '\033[1;33mUpdate available on branch %s (%s commits).\033[0m\n' "$BRANCH" "$updates"
    read -p "Start anyway without updating? [y/N]: " reply
    if [[ ! $reply =~ ^[Yy]$ ]]; then
        echo "Start aborted. Run update.sh first."; exit 0
    fi
fi

printf '\033[1;34mStarting AIHost...\033[0m\n'
PYTHONPATH="$APP_DIR/src" "$APP_DIR/venv/bin/python" -m aihost.web
