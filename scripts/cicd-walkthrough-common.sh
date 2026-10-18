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

# Construction helpers: small explicit commands; source is immutable, state stays in the cycle.
new_stage_source() {
  test -d "$ROOT/.local-apex/walkthrough/current" || { echo 'ERROR: complete infrastructure installation and explicit project/area onboarding/readiness first.' >&2; exit 1; }
  stage_source="$ROOT/.local-apex/walkthrough/current/$1"
  mkdir "$stage_source" || { echo 'ERROR: this stage was already attempted. Inspect it; cleanup is a separate explicit operation.' >&2; exit 1; }
}
verify_runtime() {
  local connection="$1" schema="$2" app="$3" kind="${4:-fresh}"
  echo "VERIFICATION URL: http://127.0.0.1:8080/ords/f?p=$app:1 — sign in as VERIFIER."
  if [ "$kind" = fresh ]; then
    echo 'Create active Hello and World entries, select them as defaults, create Hello World and refresh Greeting history.'
  else
    echo 'Use the EXISTING entries/defaults, create Hello World and refresh Greeting history. Keep existing settings unchanged.'
  fi
  echo 'Password: python3 scripts/cicd-password.py VERIFIER'
  if [ "$MODE" = --rehearse ]; then
    echo 'REHEARSAL: create a NEW explicit verification greeting through the runtime API; browser checks skipped.'
    check_result "$connection" "@\"$ROOT/deploy/operator/walkthrough_runtime.sql\" $schema $app"
  else
    pause 'Complete the verification in the browser, then press any key to publish; q leaves the attempt restricted.'
  fi
}

initial_install() {
  local target="$1" schema="$2" app="$3" fixture="${4:-none}"
  local status epoch
  status="$(bash scripts/cicd-release-step.sh "$archive" "$target" status 0)"
  printf '%s\n' "$status"
  epoch="$(printf '%s\n' "$status" | sed -n 's/^TARGET=.* EPOCH=\([0-9]*\) PHASE=.*$/\1/p' | tr -d '\r')"
  [[ "$epoch" =~ ^[0-9]+$ ]] || exit 1
  pause "Press any key to admit the EMPTY $target application target; q to quit."
  bash scripts/cicd-release-step.sh "$archive" "$target" admit "$epoch"
  epoch=$((epoch+1))
  local operation
  for operation in migrate import units verify; do
    pause "Press any key for $target initial $operation; q to quit."
    bash scripts/cicd-release-step.sh "$archive" "$target" "$operation" "$epoch"
  done
  if [ "$fixture" = sentinels ]; then
    echo 'EXPLICIT TEST FIXTURE: twenty NEW qualification snapshots for the coming upgrade comparison.'
    python3 scripts/apex_sql.py "$target" tests/sql/prepare_qualification_fixture.sql
  fi
  local kind=fresh
  if [ "$fixture" = sentinels ]; then kind=existing; fi
  verify_runtime "$target" "$schema" "$app" "$kind"
  bash scripts/cicd-release-step.sh "$archive" "$target" publish "$epoch"
  bash scripts/cicd-release-result.sh "$archive" "$target"
}
patch_install() {
  local target="$1" schema="$2" app="$3" start="$4" epoch operation
  check_result "$target" 'begin E1_CTRL.e1_release.show_status; end;
/'
  epoch="$(sed -n 's/^TARGET=.* EPOCH=\([0-9]*\) PHASE=.*$/\1/p' "$work/output" | tr -d '\r')"
  [[ "$epoch" =~ ^[0-9]+$ ]] || exit 1
  for operation in preflight admit migrate import units verify; do
    pause "Press any key for $target patch $operation (start $start); q to quit."
    bash scripts/cicd-patch-step.sh "$archive" "$target" "$operation" "$epoch" "$start"
    if [ "$operation" = admit ]; then epoch=$((epoch+1)); fi
  done
  local kind=existing
  if [ "$start" = empty ]; then kind=fresh; fi
  verify_runtime "$target" "$schema" "$app" "$kind"
  bash scripts/cicd-patch-step.sh "$archive" "$target" publish "$epoch" "$start"
  bash scripts/cicd-patch-step.sh "$archive" "$target" result "$epoch" 1.0.0
}
