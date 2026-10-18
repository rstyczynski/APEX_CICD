#!/usr/bin/env bash
# BUG-7: explicit integration-only operator sequence, never UAT teardown/repair.
set -Eeuo pipefail
ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
cd "$ROOT"
mode="${1:---live}"
case "$mode" in --live|--preflight|--rehearse) ;; *) echo 'Usage: cicd-walkthrough-I_repair.sh [--live|--preflight|--rehearse]' >&2; exit 2 ;; esac
[ "$#" -le 1 ]
for file in scripts/cicd-recovery-artifact.py scripts/cicd-recovery-step.py deploy/recovery/control.sql deploy/recovery/failed.xml deploy/recovery/repair.xml tests/integration/test_recovery.py; do test -r "$file"; done
rg -Fqx '## I. Inspect and repair one failed additive deployment' progress/E.1/cicd-walkthrough.md
if [ "$mode" = --preflight ]; then echo 'OK I: repair chapter, source files and test found; no database mutation.'; exit 0; fi
[ "$mode" != --live ] || [ -t 0 ] || { echo 'ERROR: live observation approval needs an interactive terminal.' >&2; exit 2; }
revision="$(git rev-parse HEAD)"
failed=".local-apex/releases/failed-additive-${revision:0:12}.tar"
repair=".local-apex/releases/forward-repair-${revision:0:12}.tar"
if [ ! -e "$failed" ] && [ ! -e "$repair" ]; then python3 scripts/cicd-recovery-artifact.py build "$revision"; fi
python3 scripts/cicd-recovery-artifact.py inspect "$failed"
python3 scripts/cicd-recovery-artifact.py inspect "$repair"
if [ "$mode" = --rehearse ]; then
 echo 'REHEARSAL: pre-authorized scripted failure/observation/repair proof; no browser or new human review claim.'
 python3 tests/integration/test_recovery.py "$failed" "$repair"
 exit
fi
pause() {
 local key=''
 printf '\n%s\n' "$1"
 IFS= read -r -s -n 1 key || exit 130
 printf '\n'
 case "$key" in q|Q) exit 130 ;; esac
}
python3 scripts/cicd-recovery-step.py "$failed" bootstrap
pause 'Press any key to start the integration-only additive deployment and its deliberate failure; q to stop.'
python3 scripts/cicd-recovery-step.py "$failed" fail
pause 'Open http://127.0.0.1:8080/ords/f?p=810004:1 as LAB_USER: access must be blocked. Press a key to inspect partial state; q leaves it retained.'
python3 scripts/cicd-recovery-step.py "$failed" observe
printf 'Review the retained index, failed receipt and preservation evidence. Paste REVIEWED SHA256 to authorize this exact partial state (q to stop): '
IFS= read -r approved_observation
[ "$approved_observation" != q ] && [ "$approved_observation" != Q ] || exit 130
python3 scripts/cicd-recovery-step.py "$repair" repair --approve-observation "$approved_observation"
python3 scripts/cicd-recovery-step.py "$repair" repair
echo 'PRODUCT OWNER: reopen integration application 810004 as LAB_USER. Greeting history/settings remain; ordinary access is restored.'
pause 'Inspect the repaired integration application and retained history, then press any key to finish.'
echo 'PASS result stage I_repair. UAT was not changed.'
