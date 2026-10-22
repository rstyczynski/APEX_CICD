#!/usr/bin/env python3
"""Explicit integration-only BUG-7 proof, including changed-observation rejection."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(subprocess.check_output(['git','-C',str(Path(__file__).resolve().parent),'rev-parse','--show-toplevel'],text=True).strip())
sys.path.insert(0,str(ROOT/'scripts'))
from apex_sql import run


def main():
    if len(sys.argv)!=3:raise ValueError('Usage: python3 tests/integration/test_recovery.py FAILED_ARCHIVE REPAIR_ARCHIVE')
    failed,repair=sys.argv[1:]
    step=[sys.executable,str(ROOT/'scripts/cicd-recovery-step.py')]
    def invoke(archive, operation, *extra):
        subprocess.run(step+[archive,operation,*extra],cwd=ROOT,check=True)
    invoke(failed,'bootstrap');invoke(failed,'fail');invoke(failed,'observe')
    journal=json.loads((ROOT/'.local-apex/recovery/current.json').read_text())
    spec=importlib.util.spec_from_file_location('recovery_artifact',ROOT/'scripts/cicd-recovery-artifact.py')
    a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
    repair_hash,info,_=a.inspect(Path(repair))
    # A separately labeled synthetic change must stop both client and server admission.
    print('NEGATIVE FIXTURE: create one unexpected index in integration_test only.',flush=True)
    run('create index e1_rp_unexpected on greeting_history(actor,greeting_id);',connection='integration_test')
    result=subprocess.run(step+[repair,'repair','--approve-observation',journal['observation_sha256']],cwd=ROOT,text=True,capture_output=True)
    if result.returncode==0 or 'REJECTED changed partial observation' not in result.stderr:raise ValueError('Changed observation was not rejected by controller')
    print(result.stderr,flush=True)
    try:
        run(f"begin E1_CTRL.e1_recovery.start_repair({journal['failed_epoch']},'{repair_hash}','{info['source_commit']}',e1_recovery_observation); end;\n/",connection='integration_test')
    except RuntimeError as exc:
        if 'ORA-20846' not in str(exc):raise
        print('PASS server-side recheck rejects changed partial state (ORA-20846).',flush=True)
    else:raise ValueError('Server allowed changed partial observation')
    print('NEGATIVE FIXTURE RESTORE: drop only E1_RP_UNEXPECTED; this is not the failed deployment repair.',flush=True)
    run('drop index e1_rp_unexpected;',connection='integration_test')
    invoke(repair,'repair','--approve-observation',journal['observation_sha256'])
    invoke(repair,'repair')
    result=run(f"""set serveroutput on
declare n number; begin
 select count(*) into n from E1_CTRL.e1_recovery_cases where failed_epoch={journal['failed_epoch']} and phase='repaired';
 if n<>1 then raise_application_error(-20858,'Repair case receipt missing'); end if;
 dbms_output.put_line('PASS failed and successful control case retained');
end;
/""",connection='integration_test')
    print(result)
    print('PASS BUG-7: committed DDL failure, closed runtime gate, changed-observation rejection, forward repair, preserved history and unchanged repeat. UAT untouched.')


if __name__=='__main__':
    try:main()
    except Exception as exc:sys.exit('ERROR: '+str(exc)+'\nInspect retained integration case; do not blindly repeat or reset.')
