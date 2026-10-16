#!/usr/bin/env bash
# Use-case/result companion to developer_walkthrough.md; current A result only.
set -Eeuo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
MANUAL="$ROOT/progress/E.1/developer_walkthrough.md"
MODE="${1:---live}"
case "$MODE" in
  --live|--preflight|--rehearse) ;;
  *) echo 'Usage: bash scripts/cicd-developer-walkthrough.sh [--live|--preflight|--rehearse]' >&2; exit 2 ;;
esac
if [ "$#" -gt 1 ]; then echo 'Only one mode is accepted.' >&2; exit 2; fi
if [ "$MODE" = --live ] && [ ! -t 0 ]; then echo 'ERROR: use an interactive terminal for Product Owner checkpoints.' >&2; exit 2; fi
source scripts/cicd-env.sh
work=''
cleanup() { if [ -n "$work" ]; then rm -f "$work/check.sql" "$work/output"; rmdir "$work"; fi; }
trap cleanup EXIT
trap 'exit 130' INT TERM
trap 'result=$?; printf "ERROR: developer walkthrough stopped at line %s (status %s).\n" "$LINENO" "$result" >&2' ERR
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
  printf '\nDeveloper operation target: %s\n%s\n' "$connection" "$body"
  printf '%s\n' 'whenever oserror exit failure rollback' 'whenever sqlerror exit failure rollback' \
    'set serveroutput on' "$body" "begin dbms_output.put_line('DEVELOPER_CHECK_COMPLETE'); end;" '/' 'exit' > "$work/check.sql"
  sql -nohistory -noupdates -home "$APEX_CICD_CONNECTIONS" -name "$connection" \
    @"$work/check.sql" </dev/null 2>&1 | tee "$work/output" || result=$?
  if [ "$result" -ne 0 ] || ! rg -q '^DEVELOPER_CHECK_COMPLETE\r?$' "$work/output" || \
      rg -q 'ORA-[0-9]{5}|PLS-[0-9]{5}|SP2-[0-9]+|^Error|^ERROR|^Unknown Command' "$work/output"; then
    echo "ERROR: $connection verification failed; no later stage executed." >&2; exit 1
  fi
  echo "OK: $connection internal verification completed."
}
command -v sql >/dev/null
command -v rg >/dev/null
for name in identity application_inventory component_inventory foundation_verify show_reservations; do
  test -r "$ROOT/deploy/operator/$name.sql"
done
for heading in '## A. Deliver Foundation' '## B. Deliver Hello — pending construction'; do
  if ! rg -Fqx -- "$heading" "$MANUAL"; then echo "ERROR: manual/script mismatch: $heading" >&2; exit 1; fi
done
echo 'OK: required tools/files and chapter references found. Database access is checked in A.'
if [ "$MODE" = --preflight ]; then exit 0; fi
umask 077
mkdir -p .local-apex/operator
work="$(mktemp -d "$ROOT/.local-apex/operator/developer.XXXXXX")"
echo "Use-case walkthrough: $MANUAL"
echo 'Current scope: show A’s existing runtime result. No new deployment is performed; positive release and rejection demonstrations remain pending.'
section '## A. Deliver Foundation'
pause 'Press any key to check the existing Foundation result; q to quit.'
check_result lab-dev "@\"$ROOT/deploy/operator/identity.sql\" E1_DEV_A E1_DEV_A
@\"$ROOT/deploy/operator/application_inventory.sql\"
@\"$ROOT/deploy/operator/component_inventory.sql\"
@\"$ROOT/deploy/operator/foundation_verify.sql\""
check_result lab-control "@\"$ROOT/deploy/operator/show_reservations.sql\""
echo 'PRODUCT OWNER: open http://127.0.0.1:8080/ords/f?p=810001:1'
echo 'Expected: Foundation assembly: Hello and World are not installed.'
pause 'Open that runtime URL to see the blocked incomplete application, then press any key; q to quit.'
section '## B. Deliver Hello — pending construction'
echo 'PENDING: B has reviewed Hello source; grouped developer delivery replay and later stages are not implemented.'
echo 'Positive deployments, the usable greeting and wrong-deployment protection are pending. No DEPLOYED/REJECTED outcome is claimed.'
echo 'Stopped before any B-area mutation.'
exit 3
