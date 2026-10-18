#!/usr/bin/env python3
"""BUG-6 native C-only upgrade identity experiment; preserves UAT and all business rows."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(subprocess.check_output(['git','-C',str(Path(__file__).resolve().parent),'rev-parse','--show-toplevel'],text=True).strip())
sys.path.insert(0,str(ROOT/'scripts'))
from apex_sql import run

TARGET='lab-dev-c'
APP=810003


def snapshot():
    return run('set sqlformat csv\n'+(ROOT/'tests/sql/initial_preservation_snapshot.sql').read_text(),connection=TARGET)


def main():
    if sys.argv[1:] != ['--run']:
        raise ValueError('Explicit native C upgrade experiment: python3 tests/integration/test_apex_identity.py --run')
    directory=Path(tempfile.mkdtemp(prefix='identity-review.',dir=ROOT/'.local-apex'))
    def sql(label, body):
        output=run('set serveroutput on\n'+body,connection=TARGET)
        (directory/(label+'.log')).write_text(output)
        return output
    revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    before=snapshot();(directory/'business-before.txt').write_text(before)
    try:
        run(f'@"{ROOT}/deploy/operator/import_patch.sql" E1_DEV_C 810005 E1_DEV_C WRONG "{ROOT}/apex/f810001"\n', connection=TARGET)
    except RuntimeError as exc:
        if 'ORA-20645' not in str(exc): raise
        (directory/'wrong-target.log').write_text('PASS wrong-workspace application rejected before import (ORA-20645).\n')
    else: raise ValueError('Wrong target accepted')
    owned=sql('reserve',f"""variable generation number
begin :generation:=E1_CTRL.e1_ownership.acquire('Foundation,Hello,World','BUG-6-identity','{revision}'); end;
/
begin dbms_output.put_line('GENERATION='||:generation); end;
/""")
    generation=re.search(r'^GENERATION=(\d+)',owned,re.M).group(1)
    sql('backup',f'apex export -applicationid {APP} -split -skipExportDate -expOriginalIds -expSupportingObjects N -dir "{directory}"\n')
    output=sql('saved-report',f"""declare old_report number; new_report number;
begin
 apex_session.create_session(p_app_id=>{APP},p_page_id=>10,p_username=>'LAB_USER');
 select report_id into old_report from apex_application_page_ir_rpt
 where application_id={APP} and page_id=10 and report_type='PRIMARY_DEFAULT';
 new_report:=apex_ir.clone_report(p_report_id=>old_report,p_new_name=>'BUG-6 retained report',
   p_new_owner=>'LAB_USER',p_new_is_public=>false,p_replace_report=>false);
 commit;
 dbms_output.put_line('SAVED_REPORT='||new_report);
 apex_session.delete_session;
end;
/""")
    report=re.search(r'^SAVED_REPORT=(\d+)',output,re.M).group(1)
    def identities():
        return sql('identities-current',f"""set sqlformat csv
select page_id,region_id,region_name from apex_application_page_regions where application_id={APP} order by page_id,region_id;
select report_id,report_name,report_type,application_user,report_columns from apex_application_page_ir_rpt where application_id={APP} and report_id={report};""")
    ids=identities();(directory/'identities-before.txt').write_text(ids)
    if 'BUG-6 retained report' not in ids: raise ValueError('Saved report fixture missing')
    sql('maintenance',f"""begin
 apex_util.set_workspace('E1_DEV_C');
 apex_application_admin.set_application_status({APP},apex_application_admin.c_app_restricted_access,
 p_allowed_users_list=>apex_t_varchar2('VERIFIER'),p_message=>'BUG-6 identity experiment');
 update lab_state set state='maintenance',reason='BUG-6 identity experiment' where state_key='Application';
 commit;
end;
/""")
    sql('migration',f'cd "{ROOT}"\nlb validate -changelog-file db/changelog.xml\nlb update -changelog-file db/changelog.xml\n')
    for attempt in [1,2]:
        sql(f'import-{attempt}',f'@"{ROOT}/deploy/operator/import_patch.sql" E1_DEV_C {APP} E1_DEV_C APEX-DELIVERY-LABORATORY-C "{ROOT}/apex/f810001"\n')
        if identities()!=ids: raise ValueError('Component IDs or private saved report changed')
        if snapshot()!=before: raise ValueError('Business history/configuration changed')
    sql('finish',f"""begin
 apex_session.create_session(p_app_id=>{APP},p_page_id=>10,p_username=>'LAB_USER');
 apex_ir.delete_report(p_report_id=>{report});
 apex_session.delete_session;
 update lab_state set state='ready',reason='BUG-6 verified stable replacement identities' where state_key='Application';
 apex_application_admin.set_application_status({APP},apex_application_admin.c_app_available);
 commit;
 E1_CTRL.e1_ownership.release_task('BUG-6-identity',{generation});
end;
/""")
    print('PASS BUG-6: two replacement imports retain component IDs, one private saved report and all prior history/configuration.')
    print('C now runs Hello 1.0.1; UAT was not changed. Evidence: '+str(directory.relative_to(ROOT)))


if __name__=='__main__':
    try: main()
    except (ValueError,RuntimeError,OSError,subprocess.SubprocessError) as exc:
        sys.exit('ERROR: '+str(exc)+'\nInspect retained C reservation/checkpoint before retry; no automatic reset.')
