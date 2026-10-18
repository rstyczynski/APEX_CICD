#!/usr/bin/env bash
# Manual chapter 5: integrated changelog status on preserved A lists Hello/World pending; never auto-apply them.
# Guided execution of the current manual; Oracle operations stay visible.
set -Eeuo pipefail
ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
cd "$ROOT"
MANUAL="$ROOT/progress/E.1/user_manual.md"
MODE="${1:---live}"
case "$MODE" in
  --live|--preflight|--rehearse) ;;
  *) echo 'Usage: bash scripts/cicd-operator-walkthrough.sh [--live|--preflight|--rehearse]' >&2; exit 2 ;;
esac
if [ "$#" -gt 1 ]; then echo 'Only one mode is accepted.' >&2; exit 2; fi
source scripts/cicd-env.sh
work=''
cleanup() { if [ -n "$work" ]; then rm -f "$work/step.sql" "$work/output"; rmdir "$work"; fi; }
trap cleanup EXIT
trap 'result=$?; printf "ERROR: walkthrough stopped at script line %s (status %s). Inspect the output above.\n" "$LINENO" "$result" >&2' ERR
trap 'exit 130' INT TERM

chapter() {
  local heading="$1"
  printf '\n========== MANUAL %s ==========\n' "$heading"
  awk -v heading="$heading" '
    $0 == heading {found=1; print; next}
    found && /^#/ {exit}
    found {print}
  ' "$MANUAL"
}

pause() {
  local key=''
  if [ "$MODE" = --rehearse ]; then
    echo 'REHEARSAL: keypress skipped; no human inspection claimed.'
    return
  fi
  printf '%s\n' "${1:-Press any key to execute this operation; q to quit.}"
  if ! IFS= read -r -s -n 1 key; then echo 'Input ended; stopping.' >&2; exit 130; fi
  printf '\n'
  if [ "$key" = q ] || [ "$key" = Q ]; then echo 'Stopped by operator.'; exit 130; fi
}

sql_step() {
  local connection="$1" body="$2" status=0
  printf '\nTARGET: %s\nSQLcl operation:\n%s\n' "$connection" "$body"
  pause
  # A real SQLcl script avoids interactive stdin buffering of statements.
  {
    printf '%s\n' 'whenever oserror exit failure rollback' 'whenever sqlerror exit failure rollback' \
      'set define off serveroutput on' "cd $ROOT" "$body" \
      "begin dbms_output.put_line('OPERATOR_STEP_COMPLETE'); end;" '/' 'exit'
  } > "$work/step.sql"
  sql -nohistory -noupdates -home "$APEX_CICD_CONNECTIONS" -name "$connection" \
    @"$work/step.sql" </dev/null 2>&1 | tee "$work/output" || status=$?
  if [ "$status" -ne 0 ] || ! rg -q '^OPERATOR_STEP_COMPLETE\r?$' "$work/output" || \
      rg -q 'ORA-[0-9]{5}|PLS-[0-9]{5}|SP2-[0-9]+|^Error|^ERROR|^Unknown Command|Processing has failed' "$work/output"; then
    echo "ERROR: $connection operation failed; no later operation executed." >&2
    exit 1
  fi
  echo "OK: $connection operation completed. Inspect the output above."
}

browser_step() {
  local heading="$1" url="$2"
  chapter "$heading"
  printf '\nBROWSER URL: %s\n' "$url"
  if [ "$heading" = '#### 4.1 Sign in as Developer A' ] && [ "$MODE" = --live ]; then
    echo 'COMMAND: python3 scripts/cicd-password.py DEV_A (prints only the requested password; no transcript is saved)'
    pause 'Press any key to display the local DEV_A password; q to quit.'
    python3 scripts/cicd-password.py DEV_A
  fi
  if [ "$MODE" = --rehearse ]; then
    echo 'SKIPPED: password display, browser interaction and human verification. No browser pass claimed.'
  else
    case "$heading" in
      '#### 4.1 '*|'#### 4.5 '*) pause 'Open the URL, follow the displayed chapter, then press any key to continue; q to quit.' ;;
      *) pause 'Keep your signed-in Builder tab open and follow this chapter there. Press any key when finished; q to quit. The URL above is the entry point if you need to sign in again.' ;;
    esac
    echo 'CONTINUED: browser step acknowledged by operator; not an automated browser check.'
  fi
}

# Preflight is local/read-only; it neither provisions nor resets the runtime.
command -v sql >/dev/null
command -v python3 >/dev/null
command -v rg >/dev/null
command -v diff >/dev/null
for name in identity application_inventory component_inventory foundation_verify show_reservations assert_ownership capture_current_foundation; do
  test -r "$ROOT/deploy/operator/$name.sql"
done
test -r db/changelog.xml
test -d apex/f810001
test -r .local-apex/e1-secrets.json
for heading in \
  '### 1. Select the local tools and connection store' \
  '### 2. Connect to A and identify the target' \
  '### 3. Inspect the ownership authority separately' \
  '#### 4.1 Sign in as Developer A' \
  '#### 4.2 Open application 810001' \
  '#### 4.3 Inspect the application version' \
  '#### 4.4 Inspect the Home and Login definitions' \
  '#### 4.5 Check runtime availability, then continue to SQLcl' \
  '### 5. Inspect migration state before applying anything' \
  '### 6. Capture APEX source as an operator' \
  '### 7. Review the captured changes before accepting source' \
  '### 8. Continue through the remaining delivery stages'; do
  if ! rg -Fqx -- "$heading" "$MANUAL"; then
    echo "ERROR: script/manual chapter mismatch: $heading" >&2; exit 1
  fi
done
echo 'OK: tools, required files and manual chapter mapping found. Database access is checked in chapter 2.'
if [ "$MODE" = --preflight ]; then exit 0; fi
if [ "$MODE" = --live ] && [ ! -t 0 ]; then
  echo 'ERROR: live mode requires an interactive terminal. Use --preflight for local checks.' >&2; exit 2
fi
mkdir -p .local-apex/operator
work="$(mktemp -d "$ROOT/.local-apex/operator/run.XXXXXX")"
chmod 700 "$work"
umask 077
printf 'MODE: %s\nManual: %s\n' "$MODE" "$MANUAL"
echo 'Current Foundation walkthrough only. No infrastructure reset, migration update, source replacement, commit or release is performed.'
chapter '### 1. Select the local tools and connection store'
echo 'COMMAND: sql -version'
pause
sql -version
chapter '### 2. Connect to A and identify the target'
for name in identity application_inventory component_inventory foundation_verify; do
  args=''
  if [ "$name" = identity ]; then args=' E1_DEV_A E1_DEV_A'; fi
  sql_step lab-dev "@\"$ROOT/deploy/operator/$name.sql\"$args"
done
chapter '### 3. Inspect the ownership authority separately'
sql_step lab-control "@\"$ROOT/deploy/operator/show_reservations.sql\""
# Browser instructions are read from the manual itself, not duplicated here.
for heading in \
  '#### 4.1 Sign in as Developer A' \
  '#### 4.2 Open application 810001' \
  '#### 4.3 Inspect the application version' \
  '#### 4.4 Inspect the Home and Login definitions'; do
  browser_step "$heading" 'http://127.0.0.1:8080/ords/f?p=4550:1'
done
browser_step '#### 4.5 Check runtime availability, then continue to SQLcl' 'http://127.0.0.1:8080/ords/f?p=810001:1'
chapter '### 5. Inspect migration state before applying anything'
sql_step lab-dev "@\"$ROOT/deploy/operator/identity.sql\" E1_DEV_A E1_DEV_A"
sql_step lab-dev 'lb validate -changelog-file db/changelog.xml'
sql_step lab-dev 'lb status -changelog-file db/changelog.xml'
echo 'INFO: lb update is historical initial-install context in the manual. Foundation is already installed; this inspection walkthrough does not apply migrations.'
sql_step lab-dev "@\"$ROOT/deploy/operator/component_inventory.sql\""
sql_step lab-dev "@\"$ROOT/deploy/operator/foundation_verify.sql\""
sql_step lab-dev 'select id, author, filename, exectype from databasechangelog order by orderexecuted;'
chapter '### 6. Capture APEX source as an operator'
echo 'COMMAND: mkdir -p .local-apex/captures/foundation-operator-review'
pause
mkdir -p .local-apex/captures/foundation-operator-review
sql_step lab-dev "@\"$ROOT/deploy/operator/identity.sql\" E1_DEV_A E1_DEV_A"
capture_base="$(git rev-parse HEAD)"
capture_task="foundation-capture-$$"
sql_step lab-dev "@\"$ROOT/deploy/operator/capture_current_foundation.sql\" $capture_base $ROOT/.local-apex/captures/foundation-operator-review $capture_task"
test -s .local-apex/captures/foundation-operator-review/f810001/install.sql
chapter '### 7. Review the captured changes before accepting source'
echo 'COMMAND: git status --short'
pause
git status --short
echo 'COMMAND: diff -ru apex/f810001 .local-apex/captures/foundation-operator-review/f810001'
pause
status=0
diff -ru apex/f810001 .local-apex/captures/foundation-operator-review/f810001 || status=$?
case "$status" in
  0) echo 'OK: capture matches checked-out source.' ;;
  1) echo 'REVIEW REQUIRED: differences shown above; no source was replaced or accepted automatically.' ;;
  *) echo "ERROR: diff failed with status $status; stopping." >&2; exit "$status" ;;
esac
pause 'Inspect the diff before continuing; any key continues without accepting source, q quits.'
chapter '### 8. Continue through the remaining delivery stages'
echo 'END: current working walkthrough completed. Release/integration_test/promotion remain under construction.'
if [ "$MODE" = --rehearse ]; then echo 'REHEARSAL ONLY: browser steps and human review were skipped.'; fi
