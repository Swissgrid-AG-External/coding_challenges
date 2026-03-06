#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FUNCTION_DIR="$PROJECT_DIR/function_app"

if [[ "${EUID}" -ne 0 ]]; then
  SUDO="sudo"
else
  SUDO=""
fi

echo "==> Installing system dependencies (Python, pip, curl, git, docker, compose, just)"
$SUDO apt-get update
$SUDO apt-get install -y \
  python3 \
  python3-pip \
  python3-venv \
  curl \
  ca-certificates \
  git \
  docker.io \
  just

echo "==> Enabling docker service"
$SUDO systemctl enable --now docker || true

echo "==> Adding current user to docker group"
$SUDO usermod -aG docker "$USER" || true

echo "==> Installing uv"
if ! command -v uv >/dev/null 2>&1; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi

if [[ -d "$HOME/.local/bin" ]]; then
  export PATH="$HOME/.local/bin:$PATH"
fi

echo "==> Installing Python dependencies"
cd "$FUNCTION_DIR"
python3 -m pip install --upgrade pip
if command -v uv >/dev/null 2>&1; then
  uv pip install --system -r requirements.txt
else
  python3 -m pip install -r requirements.txt
fi

echo
echo "Setup completed."
echo "If docker commands fail due to permissions, run: newgrp docker"
echo "Then start locally with:"
echo "  cd $PROJECT_DIR"
echo "  just run-once"
