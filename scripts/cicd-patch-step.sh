#!/usr/bin/env bash
# One bounded patch operation. Native SQL comes from the verified release archive.
set -Eeuo pipefail
ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
cd "$ROOT"
[ "$#" -ge 5 ] && [ "$#" -le 6 ] || { echo 'Usage: cicd-patch-step.sh ARCHIVE TARGET OPERATION EPOCH empty|1.0.0 [PROPOSAL-for-preflight-only]' >&2; exit 2; }
archive="$1"; target="$2"; operation="$3"; epoch="$4"; start="$5"
case "$target" in lab-qualify) schema=E1_QUALIFY; app=810004; alias=APEX-DELIVERY-LABORATORY-Q ;; lab-test) schema=E1_TEST; app=810005; alias=APEX-DELIVERY-LABORATORY-T ;; *) exit 2 ;; esac
case "$operation" in preflight|admit|migrate|import|units|verify|publish|result) ;; *) exit 2 ;; esac
[[ "$epoch" =~ ^[0-9]+$ ]] || exit 2
case "$start" in empty) [ "$target" = lab-qualify ] || exit 2 ;; 1.0.0) ;; *) exit 2 ;; esac
[ "$#" -eq 5 ] || [ "$operation" = preflight ] || exit 2
source scripts/cicd-env.sh
umask 077
mkdir -p .local-apex/releases/runs
work="$(mktemp -d "$ROOT/.local-apex/releases/runs/$target-patch-$operation.XXXXXX")"
payload="$work/payload"
python3 scripts/cicd-artifact.py unpack "$archive" "$payload" | tee "$work/archive.log"
cmp -s "$ROOT/scripts/cicd-patch-step.sh" "$payload/scripts/cicd-patch-step.sh" || { echo 'ERROR: patch controller differs from archive' >&2; exit 1; }
cmp -s config/areas.json "$payload/config/areas.json" || { echo 'ERROR: configuration differs' >&2; exit 1; }
# A proposed major contract goes through the same compatibility gate before any connection.
python3 "$payload/scripts/cicd-compatibility.py" "${6:-$payload/release/manifest.json}" | tee "$work/compatibility.log"
read -r base revision config hash < <(python3 - "$payload" "$archive" <<'PY'
import json,sys,hashlib
from pathlib import Path
p=Path(sys.argv[1]);m=json.loads((p/'release/manifest.json').read_text());a=json.loads((p/'artifact.json').read_text())
if m['stage']!='complete-patch': raise SystemExit('Patch archive required')
print(m['base_artifact'],a['source_commit'],a['configuration_sha256'],hashlib.sha256(Path(sys.argv[2]).read_bytes()).hexdigest())
PY
)
echo "TARGET: $target / application $app; OPERATION: $operation; START: $start; EPOCH: $epoch"
echo "PATCH SHA256: $hash; BASE SHA256: $base"
echo "TRANSCRIPT: ${work#"$ROOT/"}/operation.log"
run_sql() {
 local result=0
 cat "$work/operation.sql"
 sql -nohistory -noupdates -home "$APEX_CICD_CONNECTIONS" -name "$target" @"$work/operation.sql" </dev/null 2>&1 | tee "$work/operation.log" || result=$?
 if [ "$result" -ne 0 ] || ! rg -q '^PATCH_OPERATION_COMPLETE\r?$' "$work/operation.log" || rg -qi 'ORA-[0-9]{5}|PLS-[0-9]{5}|SP2-[0-9]+|^Error|^ERROR|^Unknown Command|Validation Failed|Processing has failed|Unexpected error running Liquibase' "$work/operation.log"; then
  echo 'ERROR: patch operation failed; ownership/partial state retained. No automatic reset or success publication.' >&2; exit 1
 fi
}
header() {
 printf '%s\n' 'whenever oserror exit failure rollback' 'whenever sqlerror exit failure rollback' 'set serveroutput on define on verify off'
 printf '@"%s/deploy/operator/identity.sql" %s %s\n' "$payload" "$schema" "$schema"
 printf '@"%s/deploy/checks/release_environment.sql"\n' "$payload"
}
footer() { printf '%s\n' "begin dbms_output.put_line('PATCH_OPERATION_COMPLETE'); end;" '/' 'exit success'; }
# Status and live fingerprint use fresh read-only transactions before any maintenance write.
if [ "$operation" = preflight ] || [ "$operation" = admit ] || [ "$operation" = result ]; then
 {
  header
  printf '%s\n' 'begin E1_CTRL.e1_release.show_status; end;' '/'
  if [ "$start" = empty ]; then
   printf '@"%s/deploy/checks/initial_target.sql"\n' "$payload"
  else
   printf '@"%s/deploy/operator/fingerprint.sql" %s\n' "$payload" "$app"
  fi
  footer
 } > "$work/operation.sql"
 run_sql
 phase="$(sed -n 's/^TARGET=.* PHASE=//p' "$work/operation.log" | tr -d '\r')"
 observed_epoch="$(sed -n 's/^TARGET=.* EPOCH=\([0-9]*\) PHASE=.*$/\1/p' "$work/operation.log" | tr -d '\r')"
 [ "$observed_epoch" = "$epoch" ] || { echo 'REJECTED: stale expected epoch' >&2; exit 1; }
 case "$phase" in ready|new) ;; *) echo 'REJECTED: active/interrupted target' >&2; exit 1 ;; esac
 live=''
 if [ "$start" != empty ]; then
  [ "$phase" = ready ] || { echo 'REJECTED: installed target is not ready' >&2; exit 1; }
  installed="$(sed -n 's/^ARTIFACT=//p' "$work/operation.log" | tr -d '\r')"
  stored="$(sed -n 's/^FINGERPRINT=//p' "$work/operation.log" | tr -d '\r')"
  live="$(sed -n '/^SH256:/p' "$work/operation.log" | tr -d '\r')"
  if [ -z "$stored" ] || [ "$stored" != "$live" ]; then
   echo 'REJECTED DRIFT: live APEX fingerprint differs from the successful receipt. No maintenance, migration or import.' >&2; exit 1
  fi
  if [ "$installed" = "$hash" ]; then
   printf '@"%s/deploy/checks/patch_integrity.sql" %s\n' "$payload" "$app" > "$work/result.sql"
   python3 scripts/apex_sql.py "$target" "$work/result.sql"
   echo 'ALREADY DELIVERED: patch versions and live APEX fingerprint match; no writes.'
   exit 0
  fi
  [ "$installed" = "$base" ] || { echo 'REJECTED: unsupported baseline artifact' >&2; exit 1; }
  [ "$operation" != result ] || { echo 'REJECTED: patch not yet installed' >&2; exit 1; }
 fi
 if [ "$operation" = preflight ]; then echo 'ACCEPTED PREFLIGHT: compatible source and unchanged supported target; no writes.'; exit 0; fi
fi
{
 header
 if [ "$operation" != admit ]; then printf '@"%s/deploy/operator/assert_release.sql" %s %s\n' "$payload" "$epoch" "$hash"; fi
 case "$operation" in
 admit)
  if [ "$start" != empty ]; then
   printf '@"%s/deploy/checks/release_integrity.sql" %s\n' "$payload" "$app"
   printf '%s\n' "declare n number; before_state varchar2(20); begin" \
    "select count(*) into n from hello_entries where not regexp_like(entry_text,'[^[:space:]]');" \
    "if n<>0 then raise_application_error(-20646,'Existing invalid Hello data requires explicit correction before patch'); end if;" \
    "select state into before_state from lab_state where state_key='Application' for update nowait;" \
    "if before_state<>'ready' then raise_application_error(-20647,'Application is not ready'); end if;" \
    "update lab_state set state='maintenance',reason='Hello patch installation' where state_key='Application';" \
    "E1_CTRL.e1_release.begin_patch($epoch,'$hash','$revision','$config','$base','$start','$live');" 'end;' '/'
  else
   printf '%s\n' "begin E1_CTRL.e1_release.begin_patch($epoch,'$hash','$revision','$config','$base','$start',null); end;" '/'
  fi ;;
 migrate)
  printf 'cd "%s"\n' "$payload"
  printf '%s\n' 'lb validate -changelog-file db/changelog.xml' 'lb update -changelog-file db/changelog.xml' 'lb status -changelog-file db/changelog.xml' ;;
 import)
  import_file=import_patch; [ "$start" != empty ] || import_file=import
  printf '@"%s/deploy/operator/%s.sql" %s %s %s %s "%s/apex/f810001"\n' "$payload" "$import_file" "$schema" "$app" "$schema" "$alias" "$payload" ;;
 units)
  printf '@"%s/deploy/checks/patch_integrity.sql" %s\n' "$payload" "$app"
  for check in composition history hello_patch; do printf '@"%s/tests/sql/%s.sql"\n' "$payload" "$check"; done ;;
 verify|publish) printf '@"%s/deploy/operator/%s_patch.sql" %s %s %s\n' "$payload" "$operation" "$epoch" "$app" "$hash" ;;
 esac
 footer
} > "$work/operation.sql"
run_sql
echo "OK: $target patch $operation from verified archive bytes."
