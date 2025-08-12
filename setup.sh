#!/usr/bin/env bash
# setup.sh — initialize a Python venv for NextBus HACS development

set -euo pipefail

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip setuptools wheel
pip install requests pytest flake8 black

echo

echo "Environment ready. Run tests with:"
echo "  source .venv/bin/activate && pytest"
