#!/usr/bin/env bash
# Read-only preflight: distinguish a clean target, expected rejection and unexpected failure.
set -Eeuo pipefail

# Kept separate from the Oracle boundary so error classification can be tested directly.
protection_outcome() {
  local kind="$1" result="$2" log="$3" expect="${4:-any}" outcome=''
  if rg -q 'ORA-[0-9]{5}|PLS-[0-9]{5}|SP2-[0-9]+|^ERROR|^Traceback' "$log"; then
    echo 'FAIL: unexpected execution error; no protection result claimed.' >&2; return 1
  fi
  if [ "$kind" = compatibility ] && [ "$result" -ne 0 ] &&
      rg -Fq 'REJECTED INCOMPATIBLE: Hello requires Foundation 1.0.0; proposed Foundation 2.0.0' "$log"; then
    outcome=incompatible
  elif [ "$kind" = drift ] && [ "$result" -ne 0 ] && rg -q '^REJECTED DRIFT:' "$log"; then
    outcome=drift
  elif [ "$kind" = drift ] && [ "$result" -eq 0 ] &&
      rg -q '^(ALREADY DELIVERED:|ACCEPTED PREFLIGHT:)' "$log" && ! rg -q '^REJECTED' "$log"; then
    outcome=clean
  else
    echo 'FAIL: specific preflight outcome missing; arbitrary errors do not pass.' >&2; return 1
  fi
  if { [ "$expect" = --expect-drift ] && [ "$outcome" != drift ]; } ||
     { [ "$expect" = --expect-clean ] && [ "$outcome" != clean ]; }; then
    echo "FAIL: expected $expect, observed $outcome." >&2; return 1
  fi
  printf '%s\n' "$outcome"
}

main() {
  ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
  cd "$ROOT"
  [ "$#" -ge 1 ] && [ "$#" -le 2 ] || { echo 'Usage: cicd-protection-check.sh compatibility|drift [--expect-clean|--expect-drift]' >&2; return 2; }
  expect="${2:-any}"
  case "$expect" in any|--expect-clean|--expect-drift) ;; *) return 2 ;; esac
  [ "$#" -eq 1 ] || [ "$1" = drift ] || return 2
  kind="$1"; case "$kind" in compatibility|drift) ;; *) exit 2 ;; esac
  archive="$(cat .local-apex/releases/patch-selected.txt)"
  umask 077
  work="$(mktemp -d .local-apex/releases/protection-$kind.XXXXXX)"
  printf '%s\n' 'set serveroutput on' 'begin E1_CTRL.e1_release.show_status; end;' '/' > "$work/status.sql"
  python3 scripts/apex_sql.py user_acceptance_test "$work/status.sql" > "$work/status.log"
  epoch="$(sed -n 's/^TARGET=.* EPOCH=\([0-9]*\) PHASE=.*$/\1/p' "$work/status.log" | tr -d '\r')"
  [[ "$epoch" =~ ^[0-9]+$ ]] || exit 1
  python3 scripts/apex_sql.py user_acceptance_test tests/sql/protection_snapshot.sql > "$work/before.txt"
  python3 scripts/apex_sql.py lab-control deploy/operator/show_release_receipts.sql > "$work/control-before.txt"
  result=0
  if [ "$kind" = compatibility ]; then
   bash scripts/cicd-patch-step.sh "$archive" user_acceptance_test preflight "$epoch" 1.0.0 release/proposals/foundation-major.json > "$work/rejection.log" 2>&1 || result=$?
  else
   bash scripts/cicd-patch-step.sh "$archive" user_acceptance_test preflight "$epoch" 1.0.0 > "$work/rejection.log" 2>&1 || result=$?
  fi
  cat "$work/rejection.log"
  outcome="$(protection_outcome "$kind" "$result" "$work/rejection.log" "$expect")" || return 1
  python3 scripts/apex_sql.py user_acceptance_test tests/sql/protection_snapshot.sql > "$work/after.txt"
  python3 scripts/apex_sql.py lab-control deploy/operator/show_release_receipts.sql > "$work/control-after.txt"
  cmp "$work/before.txt" "$work/after.txt"
  cmp "$work/control-before.txt" "$work/control-after.txt"
  case "$outcome" in
    clean) echo 'NO DRIFT: live APEX fingerprint matches the published release; preflight passed. All good.' ;;
    drift) echo 'DETECTED DRIFT: deployment rejected before maintenance, migration or import.' ;;
    incompatible) echo 'DETECTED INCOMPATIBILITY: deployment rejected before maintenance, migration or import.' ;;
  esac
  echo "PASS $kind protection: target definitions, versions, entries, configuration, history and release records unchanged. Evidence: $work"
  echo 'Open http://127.0.0.1:8080/ords/f?p=810005:1 as LAB_USER to see the retained application.'
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then main "$@"; fi
