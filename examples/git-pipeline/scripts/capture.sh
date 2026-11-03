#!/usr/bin/env bash
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
python3 scripts/lab.py capture
python3 scripts/lab.py adapt-runtime
git status --short
printf '%s\n' 'Review source, commit it, then stage against the recorded baseline and review/commit dist before opening the PR.'
