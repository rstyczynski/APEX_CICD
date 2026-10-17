#!/usr/bin/env bash
# One visible initial-release operation; every executed SQL file comes from the archive.
set -Eeuo pipefail
ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
cd "$ROOT"
if [ "$#" -ne 4 ]; then echo 'Usage: bash scripts/cicd-release-step.sh ARCHIVE lab-qualify|lab-test admit|migrate|import|units|verify|publish|status EPOCH' >&2; exit 2; fi
archive="$1"; target="$2"; operation="$3"; epoch="$4"
case "$target" in lab-qualify) schema=E1_QUALIFY; app=810004; alias=APEX-DELIVERY-LABORATORY-Q ;; lab-test) schema=E1_TEST; app=810005; alias=APEX-DELIVERY-LABORATORY-T ;; *) echo 'ERROR: unsupported target' >&2; exit 2 ;; esac
case "$operation" in admit|migrate|import|units|verify|publish|status) ;; *) echo 'ERROR: unknown operation' >&2; exit 2 ;; esac
[[ "$epoch" =~ ^[0-9]+$ ]] || { echo 'ERROR: integer epoch required' >&2; exit 2; }
source scripts/cicd-env.sh
umask 077
mkdir -p .local-apex/releases/runs
work="$(mktemp -d "$ROOT/.local-apex/releases/runs/$target-$operation.XXXXXX")"
payload="$work/payload"
python3 scripts/cicd-artifact.py unpack "$archive" "$payload" | tee "$work/archive-check.log"
# Pin the controller as well as its SQL; do not run a changed checkout controller.
cmp -s "$ROOT/scripts/cicd-release-step.sh" "$payload/scripts/cicd-release-step.sh" || { echo 'ERROR: controller differs from the archived revision' >&2; exit 1; }
artifact_hash="$(shasum -a 256 "$archive" | awk '{print $1}')"
source_commit="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["source_commit"])' "$payload/artifact.json")"
config_hash="$(shasum -a 256 "$payload/config/areas.json" | awk '{print $1}')"
cmp -s config/areas.json "$payload/config/areas.json" || { echo 'ERROR: target configuration differs from qualified inputs' >&2; exit 1; }
sql -version > "$work/sqlcl-version.log" 2>&1
rg -q '25.3.0.274.1210' "$work/sqlcl-version.log" || { echo 'ERROR: unexpected SQLcl build' >&2; exit 1; }
echo "TARGET: $target / $schema / application $app; OPERATION: $operation; EPOCH: $epoch"
echo "ARCHIVE SHA256: $artifact_hash"
echo "SOURCE COMMIT: $source_commit"
echo "PRIVATE TRANSCRIPT: ${work#"$ROOT/"}/operation.log"
{
  printf '%s\n' 'whenever oserror exit failure rollback' 'whenever sqlerror exit failure rollback' 'set serveroutput on' 'set define on verify off'
  printf '@"%s/deploy/operator/identity.sql" %s %s\n' "$payload" "$schema" "$schema"
  printf '@"%s/deploy/checks/release_environment.sql"\n' "$payload"
  if [ "$operation" != admit ] && [ "$operation" != status ]; then
    printf '@"%s/deploy/operator/assert_release.sql" %s %s\n' "$payload" "$epoch" "$artifact_hash"
  fi
  case "$operation" in
    admit) printf '@"%s/deploy/operator/begin_initial.sql" %s %s %s %s\n' "$payload" "$epoch" "$artifact_hash" "$source_commit" "$config_hash" ;;
    migrate)
      printf 'cd "%s"\n' "$payload"
      printf '%s\n' 'lb validate -changelog-file db/changelog.xml' 'lb update -changelog-file db/changelog.xml' 'lb status -changelog-file db/changelog.xml' ;;
    import)
      printf '@"%s/deploy/operator/import.sql" %s %s %s %s "%s/apex/f810001"\n' "$payload" "$schema" "$app" "$schema" "$alias" "$payload"
      printf '@"%s/deploy/checks/initial_import_blocked.sql" %s\n' "$payload" "$app" ;;
    units)
      printf '@"%s/deploy/checks/release_integrity.sql" %s\n' "$payload" "$app"
      printf '@"%s/tests/sql/composition.sql"\n@"%s/tests/sql/history.sql"\n' "$payload" "$payload" ;;
    verify|publish) printf '@"%s/deploy/operator/%s_initial.sql" %s %s %s\n' "$payload" "$operation" "$epoch" "$app" "$artifact_hash" ;;
    status) printf '%s\n' 'begin E1_CTRL.e1_release.show_status; end;' '/' ;;
  esac
  printf '%s\n' "begin dbms_output.put_line('RELEASE_OPERATION_COMPLETE'); end;" '/' 'exit success'
} > "$work/operation.sql"
echo 'SQLcl operation (archive paths):'
cat "$work/operation.sql"
result=0
sql -nohistory -noupdates -home "$APEX_CICD_CONNECTIONS" -name "$target" @"$work/operation.sql" </dev/null 2>&1 | tee "$work/operation.log" || result=$?
if [ "$result" -ne 0 ] || ! rg -q '^RELEASE_OPERATION_COMPLETE\r?$' "$work/operation.log" || \
   rg -qi 'ORA-[0-9]{5}|PLS-[0-9]{5}|SP2-[0-9]+|^Error|^ERROR|^Unknown Command|Validation Failed|Processing has failed|Unexpected error running Liquibase' "$work/operation.log"; then
  echo "ERROR: $operation failed; target ownership/partial state is retained for inspection. No automatic reset or success publication." >&2; exit 1
fi
echo "OK: $target $operation completed using verified archive bytes."
