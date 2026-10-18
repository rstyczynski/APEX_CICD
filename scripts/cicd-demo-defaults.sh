#!/usr/bin/env bash
# Optional settings-only preparation of existing C; preserves history. Not fresh-start cleanup.
set -Eeuo pipefail
ROOT="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
cd "$ROOT"
MODE="${1:---run}"
case "$MODE" in --run|--preflight) ;; *) echo 'Usage: bash scripts/cicd-demo-defaults.sh [--run|--preflight]' >&2; exit 2 ;; esac
[[ "$#" -le 1 ]]
source scripts/cicd-env.sh
command -v sql >/dev/null
for file in walkthrough_idle walkthrough_defaults identity session_root; do test -r "deploy/operator/$file.sql"; done
if [ "$MODE" = --preflight ]; then echo 'OK: cleanup tools/files found; no database access or changes.'; exit 0; fi
umask 077
mkdir -p .local-apex/operator
work="$(mktemp -d "$ROOT/.local-apex/operator/walkthrough-prepare.XXXXXX")"
echo "Preparation evidence and configuration restore SQL: ${work#"$ROOT/"}"
run_sql() {
  local connection="$1" body="$2" status=0
  printf '\nTARGET: %s\nSQLcl operations:\n%s\n' "$connection" "$body"
  printf '%s\n' 'whenever oserror exit failure rollback' 'whenever sqlerror exit failure rollback' \
    'set define off' 'set serveroutput on' "$body" "begin dbms_output.put_line('PREPARATION_STEP_COMPLETE'); end;" '/' 'exit' > "$work/step.sql"
  sql -nohistory -noupdates -home "$APEX_CICD_CONNECTIONS" -name "$connection" @"$work/step.sql" </dev/null 2>&1 | tee "$work/output.log" || status=$?
  if [ "$status" -ne 0 ] || ! rg -q '^PREPARATION_STEP_COMPLETE\r?$' "$work/output.log" || \
      rg -q 'ORA-[0-9]{5}|PLS-[0-9]{5}|SP2-[0-9]+|^Error|^ERROR|^Unknown Command' "$work/output.log"; then
    echo 'ERROR: preparation stopped. No target reset or automatic recovery attempted.' >&2; exit 1
  fi
}
# Read-only checks of every target precede the configuration change.
run_sql lab-control "@\"$ROOT/deploy/operator/walkthrough_idle.sql\""
run_sql lab-dev "@\"$ROOT/deploy/operator/identity.sql\" E1_DEV_A E1_DEV_A
@\"$ROOT/deploy/operator/foundation_verify.sql\""
run_sql lab-dev-b "@\"$ROOT/deploy/operator/identity.sql\" E1_DEV_B E1_DEV_B
@\"$ROOT/deploy/checks/hello_assembly.sql\""
run_sql lab-dev-c "@\"$ROOT/deploy/operator/identity.sql\" E1_DEV_C E1_DEV_C
@\"$ROOT/deploy/checks/published_development.sql\""
# Snapshot original defaults as executable restoration SQL; credentials are absent.
run_sql lab-dev-c "set heading off
set feedback off
set pagesize 0
set sqlformat default
set linesize 32767
spool \"$work/restore-defaults.sql\"
select 'whenever sqlerror exit failure rollback' from dual;
select 'set define off' from dual;
select q'[begin if user<>'E1_DEV_C' then raise_application_error(-20705,'Restore requires E1_DEV_C'); end if; lab_runtime.assert_ready; end;]' from dual;
select '/' from dual;
select 'update '||component||'_config set prefix='||
 case when prefix is null then 'NULL' else chr(39)||replace(prefix,chr(39),chr(39)||chr(39))||chr(39) end||
 ', default_entry_id='||coalesce(to_char(default_entry_id),'NULL')||' where config_id=1;' from
 (select 'hello' component,prefix,default_entry_id from hello_config union all
  select 'world',prefix,default_entry_id from world_config);
select 'commit;' from dual;
spool off"
history_snapshot() {
  run_sql lab-dev-c "set heading off
set feedback off
set pagesize 0
set sqlformat default
set linesize 32767
spool \"$work/$1\"
select to_char(greeting_id)||':'||rawtohex(standard_hash(json_object(* returning varchar2(4000)),'SHA256')) from greeting_history order by greeting_id;
spool off"
}
history_snapshot history-before.txt
run_sql lab-dev-c "@\"$ROOT/deploy/operator/walkthrough_defaults.sql\""
history_snapshot history-after.txt
if ! cmp -s "$work/history-before.txt" "$work/history-after.txt"; then
  echo 'ERROR: history differs during preparation; inspect the evidence (including concurrent use).' >&2; exit 1
fi
echo 'PASS preparation: deterministic defaults; complete existing history snapshots unchanged.'
echo 'A/B/C schemas, credentials, integration_test, TEST, release records and Podman resources retained.'
