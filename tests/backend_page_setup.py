"""One-time isolated native APEX baseline installation; existing names fail closed."""
from pathlib import Path
import subprocess,secrets,json,os,re
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'progress/E.5/fixtures/native-baseline'
password=secrets.token_urlsafe(24)
parts=["""whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
set define off
set sqlblanklines on
alter session set container=FREEPDB1;
create user E5_PAGE no authentication default tablespace users quota 100m on users;
grant create session, create table, create procedure, create trigger to E5_PAGE;
alter session set current_schema=E5_PAGE;
"""]
for folder in ('tables','package_specs','package_bodies','ref_constraints','triggers'):
 for p in sorted((BASE/folder).glob('*.sql')): parts.append(p.read_text())
parts.append("""
insert into lab_components values ('Foundation',1,'1.0.0');
insert into lab_components values ('Hello',1,'1.0.0');
insert into lab_components values ('World',1,'1.0.0');
insert into lab_state values ('Application',null,'ready','E5 synthetic fixture');
insert into lab_state values ('Foundation','Application','ready','E5 synthetic fixture');
insert into lab_state values ('Hello','Application','ready','E5 synthetic fixture');
insert into lab_state values ('World','Application','ready','E5 synthetic fixture');
insert into hello_entries(entry_text,active) values ('Hello','Y');
insert into world_entries(entry_text,active) values ('World','Y');
insert into hello_config(config_id,prefix,default_entry_id) select 1,null,min(entry_id) from hello_entries;
insert into world_config(config_id,prefix,default_entry_id) select 1,null,min(entry_id) from world_entries;
commit;
alter session set current_schema=SYS;
begin
 apex_instance_admin.add_workspace(p_workspace=>'E5_PAGE',p_primary_schema=>'E5_PAGE');
 apex_util.set_security_group_id(apex_util.find_security_group_id('E5_PAGE'));
end;
/
""")
parts.append("begin apex_util.create_user(p_user_name=>'VERIFIER',p_web_password=>'"+password+"',p_developer_privs=>'ADMIN:CREATE:DATA_LOADER:EDIT:HELP:MONITOR:SQL',p_change_password_on_first_use=>'N'); end;\n/\n")
parts.append("""begin
 apex_application_install.set_workspace('E5_PAGE');
 apex_application_install.set_application_id(810503);
 apex_application_install.generate_offset;
 apex_application_install.set_schema('E5_PAGE');
 apex_application_install.set_application_alias('E5-BACKEND');
end;
/
""")
parts.append((BASE/'f810003.sql').read_text())
parts.append("\nexit\n")
r=subprocess.run(['podman','--connection','apex-cicd','exec','-i','--user','oracle','apex-db','bash','-lc','sqlplus -s / as sysdba'],input='\n'.join(parts),capture_output=True,text=True,timeout=240)
output=(r.stdout+r.stderr).replace(password,'[REDACTED]')
(ROOT/'progress/E.5/tests/page-baseline-install.log').write_text(output)
if r.returncode or re.search(r'(?m)^\s*(ORA-|PLS-|SP2-)',output):raise RuntimeError(output[-2500:])
path=Path('/tmp/e5-page-session.json');path.write_text(json.dumps({'username':'VERIFIER','password':password}));path.chmod(0o600)
print('Installed isolated native app 810503; temporary login material is OS-private.')
