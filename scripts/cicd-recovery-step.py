#!/usr/bin/env python3
"""One integration-only BUG-7 operation: bootstrap, fail, observe or reviewed repair."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
import tempfile

from apex_sql import ROOT, run


def load(name, path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


archive_tool=load('recovery_artifact',ROOT/'scripts/cicd-recovery-artifact.py')
preservation=load('recovery_preservation',ROOT/'scripts/cicd-preservation.py')
STORE=ROOT/'.local-apex/recovery'
JOURNAL=STORE/'current.json'
TARGET='integration_test'
sha=lambda value:hashlib.sha256(value).hexdigest()
quote=lambda value:"'"+str(value).replace("'","''")+"'"


def fingerprint():
    result=run(f'@"{ROOT}/deploy/operator/fingerprint.sql" 810004\n',connection=TARGET)
    values=re.findall(r'^SH256:[^\r\n]+',result,re.M)
    if len(values)!=1:raise ValueError('Single integration application fingerprint required')
    return values[0]


def observation():
    text=run("set serveroutput on\nbegin dbms_output.put_line('OBS='||e1_recovery_observation); end;\n/",connection=TARGET)
    found=re.findall(r'^OBS=(.+)',text,re.M)
    if len(found)!=1:raise ValueError('Complete partial-index/migration observation required')
    return found[0].strip()


def state():
    out=run('set serveroutput on\nbegin E1_CTRL.e1_release.show_status; end;\n/',connection=TARGET)
    epoch=re.search(r'EPOCH=(\d+) PHASE=(\w+)',out)
    artifact=re.search(r'^ARTIFACT=([0-9a-f]{64})$',out,re.M)
    if not epoch or not artifact:raise ValueError('Complete current release state required')
    return int(epoch[1]),epoch[2],artifact[1]


def write_journal(value):
    tmp=JOURNAL.with_suffix('.tmp');tmp.write_text(json.dumps(value,indent=2)+'\n');tmp.chmod(0o600);tmp.replace(JOURNAL)


def observed_identity():
    return {'metadata':observation(),'fingerprint':fingerprint(),'business':preservation.snapshot(TARGET)}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('archive',type=Path);p.add_argument('operation',choices=['bootstrap','fail','observe','repair']);p.add_argument('--approve-observation')
    args=p.parse_args()
    digest,info,files=archive_tool.inspect(args.archive)
    for name,data in files.items():
        if name.startswith('scripts/') and (ROOT/name).read_bytes()!=data:raise ValueError('Recovery controller/helper differs from archived source: '+name)
    STORE.mkdir(mode=0o700,parents=True,exist_ok=True)
    work=Path(tempfile.mkdtemp(prefix=args.operation+'.',dir=STORE));payload=work/'payload';payload.mkdir()
    for name,data in files.items():
        dest=payload/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
    def sql(label, body, target=TARGET):
        print('OPERATION '+label+' AS '+target+'\n'+body,flush=True)
        try:output=run('set serveroutput on\n'+body,connection=target)
        except RuntimeError as exc:
            (work/(label+'.log')).write_text(str(exc));raise
        (work/(label+'.log')).write_text(output);print(output,flush=True);return output
    migration=lambda name:f'cd "{payload}"\nlb validate -changelog-file deploy/recovery/{name}.xml\nlb update -changelog-file deploy/recovery/{name}.xml\n'
    if args.operation=='bootstrap':
        sql('control',f'@"{payload}/deploy/recovery/control.sql"',target='lab-control')
        sql('observer',f'@"{payload}/deploy/recovery/observe.sql"')
        print('PASS recovery bootstrap: integration-only authority/observer; no UAT change.');return
    if args.operation=='fail':
        if info['kind']!='failed-additive' or JOURNAL.exists():raise ValueError('Fresh failure case and failed-additive archive required; inspect existing journal')
        epoch,phase,base=state()
        if phase!='ready':raise ValueError('Ready integration baseline required')
        sql('baseline',f'@"{ROOT}/deploy/checks/patch_integrity.sql" 810004')
        before=preservation.snapshot(TARGET)
        if len(before['history'])<20:raise ValueError('At least twenty existing sentinel history rows required; configure explicit integration fixture first')
        if 'E1_RP_HISTORY_' in observation():raise ValueError('Recovery index fixture already exists; no arbitrary retry')
        fp=fingerprint()
        sql('admit',f"""begin
 update lab_state set state='maintenance',reason='BUG-7 additive delivery' where state_key='Application';
 E1_CTRL.e1_recovery.start_failure({epoch},{quote(digest)},{quote(info['source_commit'])},{quote(base)},{quote(fp)});
end;
/""")
        journal={'phase':'installing','failed_epoch':epoch+1,'failed_hash':digest,'before':before,'fingerprint':fp,'source':info['source_commit']}
        write_journal(journal)
        try:sql('failed-migration',migration('failed'))
        except RuntimeError as exc:
            if 'ORA-20831' not in str(exc):raise
        else:raise ValueError('Expected deliberate failure was not observed')
        sql('partial-assertion',"""declare n number; begin
 select count(*) into n from user_indexes where index_name='E1_RP_HISTORY_ACTOR' and status='VALID';
 if n<>1 then raise_application_error(-20851,'Committed first DDL missing'); end if;
 select count(*) into n from databasechangelog where id='BUG7-001' and author='apex-lab';
 if n<>1 then raise_application_error(-20852,'Committed changeset identity missing'); end if;
 select count(*) into n from databasechangelog where id='BUG7-002' and author='apex-lab';
 if n<>0 then raise_application_error(-20853,'Failed changeset must not be marked successful'); end if;
 update lab_state set state='failed',reason='BUG-7 committed additive DDL; inspection required' where state_key='Application';
end;
/""")
        sql('record-failure',f"begin E1_CTRL.e1_recovery.record_failure({epoch+1},{quote(digest)},e1_recovery_observation); end;\n/")
        sql('assert-blocked',"""begin
 apex_application.g_flow_id:=810004; apex_application.g_flow_step_id:=1; apex_application.g_user:='LAB_USER';
 begin E1_CTRL.e1_release.assert_runtime; raise_application_error(-20854,'Ordinary runtime unexpectedly open');
 exception when others then if sqlcode<>-20631 then raise; end if; dbms_output.put_line('PASS ordinary runtime blocked during failure'); end;
end;
/""")
        observed=observed_identity()
        if observed['business']!=before:raise ValueError('Business fields changed during failure')
        journal.update(phase='failed',observed=observed,observation_sha256=sha(json.dumps(observed,sort_keys=True).encode()))
        write_journal(journal)
        print('EXPECTED FAILURE: committed additive DDL retained; failed receipt retained; ordinary runtime blocked.')
        print('REVIEW OBSERVATION SHA256 '+journal['observation_sha256']);return
    journal=json.loads(JOURNAL.read_text())
    current=observed_identity()
    if args.operation=='observe':
        print('OBSERVATION '+json.dumps(current,sort_keys=True))
        print('CURRENT SHA256 '+sha(json.dumps(current,sort_keys=True).encode()))
        print('REVIEWED SHA256 '+journal['observation_sha256']);return
    if info['kind']!='forward-repair' or info['source_commit']!=journal['source']:raise ValueError('Reviewed repair artifact/source required')
    if journal['phase']=='repaired':
        if digest!=journal['repair_hash'] or current!=journal['repaired_observation']:raise ValueError('Repeated repair differs from successful receipt or current state')
        epoch,phase,live_hash=state()
        if phase!='ready' or live_hash!=digest or epoch!=journal['failed_epoch']+1:raise ValueError('Repeated repair target changed')
        print('ALREADY REPAIRED: identical artifact, metadata and retained data; no writes.');return
    if journal['phase']!='failed' or args.approve_observation!=journal['observation_sha256']:raise ValueError('Explicit --approve-observation SHA256 from the inspected failure is required')
    if current!=journal['observed']:raise ValueError('REJECTED changed partial observation; no repair admission or DDL')
    sql('admit-repair',f"begin E1_CTRL.e1_recovery.start_repair({journal['failed_epoch']},{quote(digest)},{quote(info['source_commit'])},e1_recovery_observation); end;\n/")
    sql('forward-migration',migration('repair'))
    sql('completion-assertion',"""declare n number; begin
 select count(*) into n from user_indexes where index_name in ('E1_RP_HISTORY_ACTOR','E1_RP_HISTORY_DATE') and status='VALID';
 if n<>2 then raise_application_error(-20855,'Complete additive index set missing'); end if;
 select count(*) into n from databasechangelog where author='apex-lab' and id in ('BUG7-001','BUG7-003');
 if n<>2 then raise_application_error(-20856,'Forward migration history incomplete'); end if;
 select count(*) into n from databasechangelog where author='apex-lab' and id='BUG7-002';
 if n<>0 then raise_application_error(-20857,'Original failed changeset was rewritten or marked run'); end if;
end;
/""")
    after=observed_identity()
    if after['business']!=journal['before'] or after['fingerprint']!=journal['fingerprint']:raise ValueError('Repair changed retained data or application definition')
    sql('publish-repair',f"""begin
 update lab_state set state='ready',reason='BUG-7 reviewed forward repair complete' where state_key='Application';
 E1_CTRL.e1_recovery.finish_repair({journal['failed_epoch']},{quote(digest)},e1_recovery_observation,{quote(after['fingerprint'])});
 commit;
end;
/""")
    journal.update(phase='repaired',repair_hash=digest,repaired_observation=after);write_journal(journal)
    print('PASS FORWARD REPAIR: original failure retained, new successful receipt, prior twenty-plus history rows/settings preserved; no UAT change.')


if __name__=='__main__':
    try:main()
    except Exception as exc:
        sys.exit('ERROR: '+str(exc)+'\nOwnership/partial state and transcripts retained. No automatic reset or baseline adoption.')
