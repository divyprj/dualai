#!/usr/bin/env bash
set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PYTHON="$DIR/.venv/bin/python"

if [ ! -f "$PYTHON" ]; then
    if [ "$1" = "setup" ] || [ -z "$1" ]; then
        echo "[INFO] Creating virtual environment in .venv..."
        python3 -m venv "$DIR/.venv"
        "$PYTHON" "$DIR/dualai/cli.py" setup
        exit 0
    else
        echo "[ERROR] Virtual environment missing. Run './dualai.sh setup' first."
        exit 1
    fi
fi

if [ -z "$1" ]; then
    "$PYTHON" "$DIR/dualai/cli.py" --help
else
    "$PYTHON" "$DIR/dualai/cli.py" "$@"
fi
