#!/usr/bin/env bash
# Read-only current patch result, with epoch discovered from the authority.
set -Eeuo pipefail
ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
cd "$ROOT"
[ "$#" -eq 1 ] || exit 2
target="$(python3 "$ROOT/scripts/cicd_environments.py" "$1")"; case "$target" in integration_test|user_acceptance_test) ;; *) exit 2 ;; esac
archive="$(cat .local-apex/releases/patch-selected.txt)"
umask 077
work="$(mktemp -d .local-apex/releases/patch-result.XXXXXX)"
printf '%s\n' 'set serveroutput on' 'begin E1_CTRL.e1_release.show_status; end;' '/' > "$work/status.sql"
python3 scripts/apex_sql.py "$target" "$work/status.sql" | tee "$work/status.log"
epoch="$(sed -n 's/^TARGET=.* EPOCH=\([0-9]*\) PHASE=.*$/\1/p' "$work/status.log" | tr -d '\r')"
[[ "$epoch" =~ ^[0-9]+$ ]] || exit 1
bash scripts/cicd-patch-step.sh "$archive" "$target" result "$epoch" 1.0.0
