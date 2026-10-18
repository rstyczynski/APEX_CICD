#!/usr/bin/env bash
# Operator verification after explicit project/area onboarding, before A.
set -Eeuo pipefail
cd "$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
[ "$#" -eq 0 ] || { echo 'Usage: bash scripts/cicd-walkthrough-ready.sh' >&2; exit 2; }
python3 scripts/cicd-platform.py check
python3 scripts/cicd-platform.py isolation
python3 scripts/cicd-platform.py check-empty
umask 077
mkdir -p .local-apex/walkthrough/current
echo 'PASS walkthrough ready: explicit project/area onboarding checked; no applications or business history. Start A.'
