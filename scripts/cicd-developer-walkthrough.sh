#!/usr/bin/env bash
# Use-case/result companion to developer_walkthrough.md; existing A/B/C and initial release results.
# Toolchain chapter starts with APEX/ORDS and SQLcl, followed by DB/migrations and supporting tools.
set -Eeuo pipefail
ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
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
for heading in '## Applied tools and techniques' '## Prepare a repeatable walkthrough' '## A. Deliver Foundation' '## B. Deliver Hello' '## C. Deliver World and complete the assembly' '## D. Qualify the initial release' '## E. Promote the same initial artifact to TEST' '## F. Deliver the compatible Hello patch' '## G. Reject an incompatible database upgrade' '## H. Reject deployment over unexpected live change'; do
  if ! rg -Fqx -- "$heading" "$MANUAL"; then echo "ERROR: manual/script mismatch: $heading" >&2; exit 1; fi
done
for helper in cicd-patch-result.sh cicd-patch-step.sh cicd-preservation.py cicd-protection-check.sh cicd-drift-demo.py cicd-artifact.py; do test -r "$ROOT/scripts/$helper"; done
echo 'OK: required tools/files and chapter references found. Database access is checked in A.'
bash scripts/cicd-walkthrough-cleanup.sh --preflight
if [ "$MODE" = --preflight ]; then exit 0; fi
umask 077
mkdir -p .local-apex/operator
work="$(mktemp -d "$ROOT/.local-apex/operator/developer.XXXXXX")"
echo "Use-case walkthrough: $MANUAL"
echo 'Background: manual chapter "Applied tools and techniques" explains the toolchain, checks and pending release gates.'
echo 'Current scope: verify existing A/B/C, initial receipts and current patch results; then selected rejections and explicit TEST page-fixture restoration.'
echo 'PREREQUISITE: run bash scripts/cicd-walkthrough-cleanup.sh separately before this walkthrough (manual run step 2).'
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
section '## B. Deliver Hello'
pause 'Press any key to verify the existing Hello assembly; q to quit.'
check_result lab-dev-b "@\"$ROOT/deploy/operator/identity.sql\" E1_DEV_B E1_DEV_B
@\"$ROOT/deploy/operator/component_inventory.sql\"
@\"$ROOT/deploy/checks/hello_assembly.sql\""
echo 'VERIFIED EXISTING RESULT: B remains blocked while World is missing.'
echo 'PRODUCT OWNER: open http://127.0.0.1:8080/ords/f?p=810002:1'
pause 'See the World-not-installed message, then press any key; q to quit.'
section '## C. Deliver World and complete the assembly'
pause 'Press any key to verify the published development assembly; q to quit.'
check_result lab-dev-c "@\"$ROOT/deploy/operator/identity.sql\" E1_DEV_C E1_DEV_C
@\"$ROOT/deploy/operator/component_inventory.sql\"
@\"$ROOT/deploy/checks/published_development.sql\""
echo 'VERIFIED EXISTING RESULT: C development application, supported 1.0.0 / 1.0.1 / 1.0.0 components.'
echo 'PRODUCT OWNER: open http://127.0.0.1:8080/ords/f?p=810003:1 and sign in as LAB_USER.'
echo 'Select Hello/World, Create greeting, reopen Greeting history and Installed components.'
pause 'Use the application to see its result, then press any key; q to quit.'
archive="$(cat .local-apex/releases/initial-selected.txt)"
initial_hash="$(shasum -a 256 "$archive" | awk '{print $1}')"
section '## D. Qualify the initial release'
pause 'Press any key to verify the retained initial archive/receipts; q to quit.'
python3 scripts/cicd-artifact.py inspect "$archive"
check_result lab-control "@\"$ROOT/deploy/operator/show_initial_proof.sql\" $initial_hash"
echo 'PRODUCT OWNER: open http://127.0.0.1:8080/ords/f?p=810004:1 as LAB_USER. The live area now runs the later patch.'
pause 'View the current application; initial delivery is evidenced by the retained receipts, then press any key; q to quit.'
section '## E. Promote the same initial artifact to TEST'
echo 'VERIFIED HISTORICAL RESULT: the TEST epoch-1 receipt above has the same initial archive hash.'
echo 'PRODUCT OWNER: open http://127.0.0.1:8080/ords/f?p=810005:1 as LAB_USER; it now runs 1.0.1.'
pause 'View TEST, then press any key for current patch verification; q to quit.'
section '## F. Deliver the compatible Hello patch'
pause 'Press any key to verify the existing qualified/promoted patch and retained fields; q to quit.'
bash scripts/cicd-patch-result.sh lab-qualify
bash scripts/cicd-patch-result.sh lab-test
python3 scripts/cicd-preservation.py compare lab-test .local-apex/releases/test-initial-preservation.json
python3 scripts/apex_sql.py lab-test tests/sql/hello_patch.sql
echo 'PRODUCT OWNER: open http://127.0.0.1:8080/ords/f?p=810005:1; create a greeting, refresh history and inspect Installed components.'
pause 'Use TEST and see Foundation 1.0.0 / Hello 1.0.1 / World 1.0.0, then press any key; q to quit.'
section '## G. Reject an incompatible database upgrade'
pause 'Press any key to submit the incompatible Foundation-major proposal; q to quit.'
bash scripts/cicd-protection-check.sh compatibility
echo 'PRODUCT OWNER: open http://127.0.0.1:8080/ords/f?p=810005:1; the existing greeting/history application still works.'
pause 'See the retained application after rejection, then press any key; q to quit.'
section '## H. Reject deployment over unexpected live change'
pause 'Press any key to save TEST and install the controlled page-drift fixture; q to quit.'
python3 scripts/cicd-drift-demo.py inject
echo 'PRODUCT OWNER: open http://127.0.0.1:8080/ords/f?p=810005:1 and re-login if needed; see DIRECT CHANGE - deployment must stop.'
pause 'View the changed page, then press any key to attempt redeployment preflight; q leaves the fixture active for explicit restoration.'
bash scripts/cicd-protection-check.sh drift
pause 'Reopen TEST to see the changed page/history retained, then press any key for the separate RESTORE operation; q leaves the fixture active.'
python3 scripts/cicd-drift-demo.py restore
bash scripts/cicd-patch-result.sh lab-test
echo 'PRODUCT OWNER: reopen http://127.0.0.1:8080/ords/f?p=810005:1; re-login if needed. The banner is gone and history remains.'
pause 'View the restored application, then press any key to finish; q to quit.'
echo 'PASS selected walkthrough: initial receipts, Hello patch, retained fields, incompatible proposal rejection, live drift rejection and explicit restoration.'
echo 'OPEN E.1 WORK: broader concurrency, complete maintenance fencing, schema-drift coverage and failed-additive-deployment repair. No sprint closure claimed.'
