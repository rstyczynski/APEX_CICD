#!/usr/bin/env bash
# Read-only inspection of an existing initial release; never installs or resets a target.
set -Eeuo pipefail
ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
cd "$ROOT"
[ "$#" -eq 2 ] || { echo 'Usage: bash scripts/cicd-release-result.sh ARCHIVE lab-qualify|lab-test' >&2; exit 2; }
archive="$1"; target="$2"
case "$target" in lab-qualify) schema=E1_QUALIFY; app=810004 ;; lab-test) schema=E1_TEST; app=810005 ;; *) echo 'ERROR: unsupported target' >&2; exit 2 ;; esac
umask 077
mkdir -p .local-apex/operator
work="$(mktemp -d "$ROOT/.local-apex/operator/release-result.XXXXXX")"
python3 scripts/cicd-artifact.py unpack "$archive" "$work/payload"
expected="$(shasum -a 256 "$archive" | awk '{print $1}')"
bash scripts/cicd-release-step.sh "$archive" "$target" status 0 | tee "$work/status.log"
rg -q "^TARGET=$schema APP=$app EPOCH=[0-9]+ PHASE=ready" "$work/status.log" || { echo 'REJECTED: target has no published ready result.' >&2; exit 1; }
rg -q "^ARTIFACT=$expected" "$work/status.log" || { echo 'REJECTED: existing target belongs to a different artifact; use a supported upgrade path.' >&2; exit 1; }
{
 printf '@"%s/deploy/checks/release_integrity.sql" %s\n' "$work/payload" "$app"
 printf '%s\n' 'declare n number; begin' \
   "select count(*) into n from lab_state where state_key='Application' and state='ready';" \
   "if n<>1 then raise_application_error(-20636,'Application root is not ready'); end if; end;" '/' 'commit;'
 printf '@"%s/deploy/operator/fingerprint.sql" %s\n' "$work/payload" "$app"
} > "$work/check.sql"
python3 scripts/apex_sql.py "$target" "$work/check.sql" | tee "$work/live.log"
stored="$(sed -n 's/^FINGERPRINT=//p' "$work/status.log" | tr -d '\r')"
live="$(sed -n '/^SH256:/p' "$work/live.log" | tr -d '\r')"
if [ -z "$stored" ] || [ "$live" != "$stored" ]; then
 echo 'REJECTED: live APEX fingerprint differs from the published receipt; no deployment or overwrite performed.' >&2; exit 1
fi
echo "VERIFIED EXISTING INITIAL RESULT: $target; versions, ready state and live APEX fingerprint match."
echo "QUALIFIED/PROMOTED SHA256: $expected"
