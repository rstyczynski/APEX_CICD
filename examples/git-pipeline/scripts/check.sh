#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
python3 -m py_compile scripts/check_pr.py scripts/lab.py
for script in scripts/*.sh; do bash -n "$script"; done
test -f .dbtools/project.config.json
test -d src/database
test -f dist/install.sql
test -f pipeline.json
printf '%s\n' 'PASS source layout and script syntax'
