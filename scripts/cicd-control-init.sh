#!/usr/bin/env bash
# Project administrator: control schema/packages only; never developer/target areas.
set -Eeuo pipefail
cd "$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
[ "$#" -eq 0 ] || { echo 'Usage: bash scripts/cicd-control-init.sh' >&2; exit 2; }
echo 'PROJECT CONTROL: create/check E1_CTRL and its named operator connection.'
python3 scripts/cicd-platform.py control-identity
echo 'PROJECT CONTROL: install ownership and release packages; no area users/grants.'
python3 scripts/apex_sql.py lab-control deploy/control.sql
python3 scripts/apex_sql.py lab-control deploy/release_control.sql
echo 'PASS project control: E1_CTRL only. Provision each named area separately.'
