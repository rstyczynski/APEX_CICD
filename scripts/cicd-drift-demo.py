#!/usr/bin/env python3
"""Controlled TEST-only page drift fixture and explicit restoration, not release repair."""
import hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
from apex_sql import ROOT,run

STORE=ROOT/'.local-apex/releases'
POINTER=STORE/'drift-active.json'
TARGET='lab-test'
APP=810005

def fingerprint():
    text=run(f'@"{ROOT}/deploy/operator/fingerprint.sql" {APP}\n',connection=TARGET)
    found=re.findall(r'^SH256:[^\r\n]+',text,re.M)
    if len(found)!=1: raise ValueError('Single live fingerprint required')
    return found[0]

def identity():
    output=run('begin E1_CTRL.e1_release.show_status; end;\n/',connection=TARGET)
    if not re.search(r'TARGET=E1_TEST APP=810005 EPOCH=\d+ PHASE=ready',output): raise ValueError('Ready retained TEST required')
    return output

def import_fixture(directory,offset):
    # Reuse the existing target offset. Generated Oracle source stays unchanged.
    sql=f'''@"{ROOT}/deploy/operator/identity.sql" E1_TEST E1_TEST
begin
 apex_util.set_workspace('E1_TEST');
 apex_application_install.set_workspace('E1_TEST');
 apex_application_install.set_application_id(810005);
 apex_application_install.set_schema('E1_TEST');
 apex_application_install.set_application_alias('APEX-DELIVERY-LABORATORY-T');
 apex_application_install.set_offset({offset});
end;
/
@"{directory}/install.sql"
'''
    print('SQLcl: map existing TEST application/offset, execute native fixture install.sql unchanged.')
    return run(sql,connection=TARGET)

def snapshot():
    return run(f'@"{ROOT}/tests/sql/initial_preservation_snapshot.sql"',connection=TARGET)

def main(action):
    if action=='inject':
        if POINTER.exists() and json.loads(POINTER.read_text())['phase']!='restored':
            raise ValueError('An earlier demonstration remains active; inspect/restore it first')
        archive=(STORE/'patch-selected.txt').read_text().strip()
        state=identity();epoch=re.search(r'EPOCH=(\d+)',state).group(1)
        subprocess.run(['bash','scripts/cicd-patch-step.sh',archive,TARGET,'result',epoch,'1.0.0'],cwd=ROOT,check=True)
        fixture=ROOT/'tests/fixtures/drift-changed/f810001'
        # Require the reviewed fixture; neither modified nor untracked source is accepted.
        if subprocess.check_output(['git','status','--porcelain','--untracked-files=all','--','tests/fixtures/drift-changed'],cwd=ROOT).strip():
            raise ValueError('Commit/review the native demonstration fixture first')
        work=Path(tempfile.mkdtemp(prefix='drift-demo.',dir=STORE))
        before=fingerprint(); saved=snapshot()
        (work/'data-before.txt').write_text(saved)
        print('SQLcl: capture the current TEST application, without business data, for exact restoration.')
        (work/'capture.log').write_text(run(f'apex export -applicationid {APP} -split -skipExportDate -expOriginalIds -expSupportingObjects N -dir "{work}"\n',connection=TARGET))
        baseline=work/f'f{APP}'
        source=(baseline/'application/create_application.sql').read_text()
        offset=re.search(r'p_default_id_offset=>(\d+)',source).group(1)
        journal={'phase':'prepared','work':str(work.relative_to(ROOT)),'epoch':epoch,'state':state,'before':before,'offset':offset}
        POINTER.write_text(json.dumps(journal,indent=2)+'\n')
        (work/'inject.log').write_text(import_fixture(fixture,offset))
        changed=fingerprint()
        if changed==before: raise ValueError('Fixture did not produce actual APEX drift')
        if snapshot()!=saved or identity()!=state: raise ValueError('Fixture changed business data or release records')
        journal.update(phase='changed',changed=changed)
        POINTER.write_text(json.dumps(journal,indent=2)+'\n')
        print('DIRECT PAGE CHANGE INSTALLED: version and release receipt unchanged; live fingerprint differs.')
        print('Open http://127.0.0.1:8080/ords/f?p=810005:1 to see DIRECT CHANGE — deployment must stop.')
        print('Next: bash scripts/cicd-protection-check.sh drift; restoration is a separate explicit operation.')
    elif action=='restore':
        journal=json.loads(POINTER.read_text());work=ROOT/journal['work']
        if journal['phase']!='changed': raise ValueError('A completed changed fixture is required; inspect interrupted work manually')
        if identity()!=journal['state'] or fingerprint()!=journal['changed']:
            raise ValueError('Target changed again; refusing to overwrite unexplained edits or release changes')
        saved=snapshot()
        (work/'data-before-restore.txt').write_text(saved)
        (work/'restore.log').write_text(import_fixture(work/f'f{APP}',journal['offset']))
        if fingerprint()!=journal['before'] or snapshot()!=saved or identity()!=journal['state']:
            raise ValueError('Restoration does not match the original successful receipt/data')
        journal['phase']='restored';POINTER.write_text(json.dumps(journal,indent=2)+'\n')
        print('RESTORED exact pre-demonstration APEX definition; original receipt/fingerprint, settings and history preserved.')
    else:
        raise ValueError('Usage: cicd-drift-demo.py inject|restore')

if __name__=='__main__':
    try: main(sys.argv[1] if len(sys.argv)==2 else '')
    except (ValueError,OSError,KeyError,RuntimeError,subprocess.SubprocessError) as exc:
        sys.exit('ERROR: '+str(exc))
