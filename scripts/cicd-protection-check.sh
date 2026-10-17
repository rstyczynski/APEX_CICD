#!/usr/bin/env bash
# Exercise the actual preflight rejection, comparing target content and control records.
set -Eeuo pipefail
ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
cd "$ROOT"
[ "$#" -eq 1 ] || { echo 'Usage: cicd-protection-check.sh compatibility|drift' >&2; exit 2; }
kind="$1"; case "$kind" in compatibility|drift) ;; *) exit 2 ;; esac
archive="$(cat .local-apex/releases/patch-selected.txt)"
umask 077
work="$(mktemp -d .local-apex/releases/protection-$kind.XXXXXX)"
printf '%s\n' 'begin E1_CTRL.e1_release.show_status; end;' '/' > "$work/status.sql"
python3 scripts/apex_sql.py lab-test "$work/status.sql" > "$work/status.log"
epoch="$(sed -n 's/^TARGET=.* EPOCH=\([0-9]*\) PHASE=.*$/\1/p' "$work/status.log" | tr -d '\r')"
[[ "$epoch" =~ ^[0-9]+$ ]] || exit 1
python3 scripts/apex_sql.py lab-test tests/sql/protection_snapshot.sql > "$work/before.txt"
python3 scripts/apex_sql.py lab-control deploy/operator/show_release_receipts.sql > "$work/control-before.txt"
expected='REJECTED DRIFT:'
if [ "$kind" = compatibility ]; then expected='REJECTED INCOMPATIBLE: Hello requires Foundation 1.0.0; proposed Foundation 2.0.0'; fi
set +e
if [ "$kind" = compatibility ]; then
 bash scripts/cicd-patch-step.sh "$archive" lab-test preflight "$epoch" 1.0.0 release/proposals/foundation-major.json > "$work/rejection.log" 2>&1
else
 bash scripts/cicd-patch-step.sh "$archive" lab-test preflight "$epoch" 1.0.0 > "$work/rejection.log" 2>&1
fi
result=$?
set -e
cat "$work/rejection.log"
[ "$result" -ne 0 ] && rg -Fq "$expected" "$work/rejection.log" || { echo 'FAIL: specific rejection missing; arbitrary errors do not pass.' >&2; exit 1; }
python3 scripts/apex_sql.py lab-test tests/sql/protection_snapshot.sql > "$work/after.txt"
python3 scripts/apex_sql.py lab-control deploy/operator/show_release_receipts.sql > "$work/control-after.txt"
cmp "$work/before.txt" "$work/after.txt"
cmp "$work/control-before.txt" "$work/control-after.txt"
echo "PASS $kind protection: specific rejection before maintenance/migration/import; target definitions, versions, entries, configuration, history and release records unchanged. Evidence: $work"
echo 'Open http://127.0.0.1:8080/ords/f?p=810005:1 as LAB_USER to see the retained application.'
