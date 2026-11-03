#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
python3 scripts/lab.py release "$1"
