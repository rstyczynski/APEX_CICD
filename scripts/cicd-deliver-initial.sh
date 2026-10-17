#!/usr/bin/env bash
# Initial-only operator sequence. Existing matching results are verified without writes.
set -Eeuo pipefail
ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
cd "$ROOT"
[ "$#" -eq 2 ] || { echo 'Usage: bash scripts/cicd-deliver-initial.sh ARCHIVE lab-qualify|lab-test' >&2; exit 2; }
archive="$1"; target="$2"
case "$target" in lab-qualify) app=810004 ;; lab-test) app=810005 ;; *) echo 'ERROR: unsupported target' >&2; exit 2 ;; esac
status="$(bash scripts/cicd-release-step.sh "$archive" "$target" status 0)"
printf '%s\n' "$status"
phase="$(printf '%s\n' "$status" | sed -n 's/^TARGET=.* PHASE=//p' | tr -d '\r')"
epoch="$(printf '%s\n' "$status" | sed -n 's/^TARGET=.* EPOCH=\([0-9]*\) PHASE=.*$/\1/p' | tr -d '\r')"
installed="$(printf '%s\n' "$status" | sed -n 's/^ARTIFACT=//p' | tr -d '\r')"
expected="$(shasum -a 256 "$archive" | awk '{print $1}')"
if [ "$phase" = ready ] && [ "$installed" = "$expected" ]; then
 bash scripts/cicd-release-result.sh "$archive" "$target"
 echo 'ALREADY DELIVERED: verified the existing result; no migrations/imports or data changes.'
 exit 0
fi
case "$phase" in new|ready) ;; *) echo 'ERROR: active/interrupted attempt; inspect it and use its explicit operator steps. No automatic recovery.' >&2; exit 1 ;; esac
[[ "$epoch" =~ ^[0-9]+$ ]] || { echo 'ERROR: missing epoch' >&2; exit 1; }
[ -t 0 ] || { echo 'ERROR: fresh delivery needs an interactive terminal; use the manual atomic steps for automation.' >&2; exit 2; }
pause() {
 local key=''; printf '\n%s\n' "$1"
 IFS= read -r -s -n 1 key || exit 130
 printf '\n'; case "$key" in q|Q) echo 'Stopped; any admitted ownership remains for inspection.'; exit 130 ;; esac
}
echo 'Manual: progress/E.1/user_manual.md — Initial release: build, qualify and promote.'
pause 'Press any key to admit an EMPTY application target; q to quit. This never resets an existing target.'
bash scripts/cicd-release-step.sh "$archive" "$target" admit "$epoch"
epoch=$((epoch+1))
for operation in migrate import units verify; do
 pause "Press any key for $operation (archive SQL is printed); q to quit."
 bash scripts/cicd-release-step.sh "$archive" "$target" "$operation" "$epoch"
done
echo "Open http://127.0.0.1:8080/ords/f?p=$app:1 and sign in as VERIFIER."
echo 'Use the manual runtime steps: create active Hello/World, configure both defaults, create Hello World, reopen/refresh history.'
echo 'Retrieve only the verifier password locally: python3 scripts/cicd-password.py VERIFIER'
pause 'After browser verification, press any key to publish; q leaves the attempt protected for inspection.'
bash scripts/cicd-release-step.sh "$archive" "$target" publish "$epoch"
bash scripts/cicd-release-result.sh "$archive" "$target"
