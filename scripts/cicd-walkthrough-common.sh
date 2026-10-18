#!/usr/bin/env bash
# Sourced helpers for the A–H result stages; no stage operations live here.
set -Eeuo pipefail
ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
cd "$ROOT"
MANUAL="$ROOT/progress/E.1/cicd-walkthrough.md"
MODE="${1:---live}"
case "$MODE" in
  --live|--preflight|--rehearse) ;;
  *) printf 'Usage: bash %s [--live|--preflight|--rehearse]\n' "${BASH_SOURCE[1]}" >&2; exit 2 ;;
esac
if [ "$#" -gt 1 ]; then echo 'Only one mode is accepted.' >&2; exit 2; fi
if [ "$MODE" = --live ] && [ ! -t 0 ]; then echo 'ERROR: use an interactive terminal for Product Owner checkpoints.' >&2; exit 2; fi
source scripts/cicd-env.sh
work=''
cleanup() { if [ -n "$work" ]; then rm -f "$work/check.sql" "$work/output"; rmdir "$work"; fi; }
trap cleanup EXIT
trap 'exit 130' INT TERM
trap 'result=$?; printf "ERROR: results walkthrough stopped at line %s (status %s).\n" "$LINENO" "$result" >&2' ERR
pause() {
  local key=''
  if [ "$MODE" = --rehearse ]; then echo 'REHEARSAL: pause/human viewing skipped; no browser verification claimed.'; return; fi
  printf '\n%s\n' "$1"
  if ! IFS= read -r -s -n 1 key; then echo 'Input ended; stopping.' >&2; exit 130; fi
  printf '\n'
  case "$key" in q|Q) echo 'Stopped by operator.'; exit 130 ;; esac
}
section() {
  local heading="$1"
  if ! rg -Fqx -- "$heading" "$MANUAL"; then echo "ERROR: manual/script mismatch: $heading" >&2; exit 1; fi
  awk -v heading="$heading" '$0==heading {found=1; print; next} found && /^## / {exit} found {print}' "$MANUAL"
}
check_result() {
  local connection="$1" body="$2" result=0
  printf '\nOperation target: %s\n%s\n' "$connection" "$body"
  printf '%s\n' 'whenever oserror exit failure rollback' 'whenever sqlerror exit failure rollback' \
    'set serveroutput on' "$body" "begin dbms_output.put_line('WALKTHROUGH_CHECK_COMPLETE'); end;" '/' 'exit' > "$work/check.sql"
  sql -nohistory -noupdates -home "$APEX_CICD_CONNECTIONS" -name "$connection" \
    @"$work/check.sql" </dev/null 2>&1 | tee "$work/output" || result=$?
  if [ "$result" -ne 0 ] || ! rg -q '^WALKTHROUGH_CHECK_COMPLETE\r?$' "$work/output" || \
      rg -q 'ORA-[0-9]{5}|PLS-[0-9]{5}|SP2-[0-9]+|^Error|^ERROR|^Unknown Command' "$work/output"; then
    echo "ERROR: $connection verification failed; no later stage executed." >&2; exit 1
  fi
  echo "OK: $connection internal verification completed."
}
# Each stage declares its own chapter and files before any Oracle access.
prepare_stage() {
  HEADING="$1"
  shift
  command -v sql >/dev/null
  command -v rg >/dev/null
  command -v python3 >/dev/null
  command -v shasum >/dev/null
  test -r "$MANUAL"
  rg -Fqx -- "$HEADING" "$MANUAL"
  local required
  for required in "$@"; do test -r "$ROOT/$required"; done
  printf 'OK: %s — local tools/files/chapter found.\n' "$HEADING"
  if [ "$MODE" = --preflight ]; then exit 0; fi
  umask 077
  mkdir -p "$ROOT/.local-apex/operator"
  work="$(mktemp -d "$ROOT/.local-apex/operator/walkthrough.XXXXXX")"
  section "$HEADING"
}
