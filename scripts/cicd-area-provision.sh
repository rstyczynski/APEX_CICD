#!/usr/bin/env bash
# Privileged operator: provision exactly ONE assigned area, not every developer.
set -Eeuo pipefail
cd "$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
[ "$#" -eq 1 ] || { echo 'Usage: bash scripts/cicd-area-provision.sh lab-dev|lab-dev-b|lab-dev-c|integration_test|user_acceptance_test' >&2; exit 2; }
case "$1" in lab-dev|lab-dev-b|lab-dev-c|integration_test|user_acceptance_test|lab-qualify|lab-test) ;; *) echo 'ERROR: select one declared area' >&2; exit 2 ;; esac
echo "OPERATOR PROVISIONING: only $1 schema, workspace, workspace accounts, delivery grants and automation connection."
python3 scripts/cicd-platform.py provision "$1"
python3 scripts/cicd-isolation.py identity "$1"
echo "PASS assigned area: $1. No applications/migrations/business data installed."
