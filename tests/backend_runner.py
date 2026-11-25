#!/usr/bin/env python3
"""Prepared-host E.5 backend checks; fixed isolated schema, OS authentication."""
from pathlib import Path
import json
import re
import subprocess
import sys
import os
import secrets
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(os.environ.get('APEX_TEST_EVIDENCE_DIR', str(ROOT / 'progress/E.5/tests')))
API = ROOT / 'examples/testable-backend/sql/hello_entry_api.sql'

def sql(body, name):
    password = secrets.token_hex(24)
    prefix = f"""whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
set pagesize 0
set linesize 32767
set long 10000000
set longchunksize 32767
set feedback off
set heading off
set verify off
set trimspool on
set sqlblanklines on
set serveroutput on
alter session set container=FREEPDB1;
alter user E5_TEST identified by "{password}" account unlock;
connect E5_TEST/"{password}"@//localhost:1521/FREEPDB1
set serveroutput on
alter session set nls_language='AMERICAN';
alter session set nls_date_language='AMERICAN';
alter session set time_zone='+00:00';
"""
    try:
        result = subprocess.run(['podman', '--connection', 'apex-cicd', 'exec', '-i', '--user', 'oracle', 'apex-db', 'bash', '-lc', 'sqlplus -s / as sysdba'], input=prefix+body+"\nprompt E5_COMPLETE\nexit\n", capture_output=True, text=True, timeout=180)
    finally:
        cleanup = subprocess.run(['podman', '--connection', 'apex-cicd', 'exec', '-i', '--user', 'oracle', 'apex-db', 'bash', '-lc', 'sqlplus -s / as sysdba'], input="whenever sqlerror exit failure\nalter session set container=FREEPDB1;\nalter user E5_TEST no authentication;\nexit\n",capture_output=True,text=True,timeout=30)
    assert cleanup.returncode==0 and not re.search(r"ORA-|SP2-", cleanup.stdout+cleanup.stderr), "Test account cleanup failed"
    output = (result.stdout + result.stderr).replace(password, "[REDACTED]")
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT / name).write_text(output)
    if result.returncode or re.search(r'(?m)^\s*(ORA-|PLS-|SP2-|Warning:)', output) or 'E5_COMPLETE' not in output:
        raise RuntimeError(output[-3000:])
    return output

def run(paths, name, coverage=False):
    arguments = "a_paths=>e5_ut.ut_varchar2_list(" + ','.join("'e5_test.test_hello_entry_api"+('.'+p if p else '')+"'" for p in paths) + ')'
    if coverage:
        arguments += ",a_reporter=>e5_ut.ut_coverage_sonar_reporter(),a_include_objects=>e5_ut.ut_varchar2_list('E5_TEST.HELLO_ENTRY_API')"
    output = sql('select * from table(e5_ut.ut.run('+arguments+'));',name)
    if not coverage:
        assert re.search(r'\b[1-9][0-9]* tests?, 0 failed, 0 errored', output), output
    return output

def unit():
    run([''],'utplsql-full.log')
    print('PASS real utPLSQL suite')

def integration():
    before=sql("select entry_id||':'||entry_text||':'||active from hello_entries order by entry_id;",'rows-before.log')
    run(['rejects_active','rejects_long','accepts_limit','rejects_blank','trims_text'],'utplsql-reordered.log')
    run([''],'utplsql-repeat.log')
    after=sql("select entry_id||':'||entry_text||':'||active from hello_entries order by entry_id;",'rows-after.log')
    assert before==after, 'Fixture leaked rows or changed sentinel'
    sql((ROOT/'tests/sql/backend/structural_cleanup.sql').read_text(),'structural-cleanup.log')
    def coverage(paths,name):
        output=run(paths,name,True)
        start=output.index('<coverage');end=output.index('</coverage>')+len('</coverage>')
        xml=output[start:end];(OUT/name.replace('.log','.xml')).write_text(xml)
        lines=ET.fromstring(xml).findall('.//lineToCover')
        assert lines, 'Empty coverage denominator'
        return {'covered':sum(e.attrib['covered']=='true' for e in lines),'executable':len(lines)}
    baseline=coverage(['trims_text','rejects_blank','accepts_limit'],'coverage-before.log')
    improved=coverage([''],'coverage-after.log')
    assert improved['executable']==baseline['executable'] and improved['covered']>baseline['covered'], (baseline,improved)
    original=API.read_text()
    # Mutate only the isolated E5_TEST package; always restore it.
    mutant=original.replace('values (trim(p_text), p_active)', 'values (p_text, p_active)')
    assert mutant!=original
    try:
        sql(mutant,'mutant-install.log')
        output=sql("select * from table(e5_ut.ut.run('e5_test.test_hello_entry_api.trims_text'));",'mutation-detected.log')
        assert re.search(r'1 test[s]?, 1 failed, 0 errored',output), output
    finally:
        sql(original,'mutant-restored.log')
    unit()
    (OUT/'backend-results.json').write_text(json.dumps({'coverage_before':baseline,'coverage_after':improved,'repeat_reorder':'passed','unrelated_rows':'unchanged','structural_cleanup':'passed','mutation':'detected and restored','page':'outside this backend-only run; verified separately by IT4 and browser observations','fixture':'isolated E5_TEST table, not full application triggers'},indent=2)+'\n')
    print('PASS runtime isolation, structural cleanup, mutation detection and coverage improvement')

if __name__=='__main__':
    {'unit':unit,'integration':integration}[sys.argv[1]]()
