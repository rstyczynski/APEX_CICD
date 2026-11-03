#!/usr/bin/env python3
"""Prepare only the named E.3 example checkout and a new disposable target."""
from pathlib import Path
import json
import os
import secrets as random
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
from apex_sql import run, secrets

LOCAL = ROOT / '.local-apex/e3'
REPO = LOCAL / 'repo'


def main():
    LOCAL.mkdir(exist_ok=True)
    REPO.mkdir(exist_ok=True)
    config_file = LOCAL / 'lab.json'
    if config_file.exists():
        raise ValueError('E.3 already prepared; inspect retained resources, do not overwrite')
    private = secrets()
    run("""declare n number; begin
select count(*) into n from dba_users where username='E3_TARGET';
if n>0 then raise_application_error(-20931,'E3_TARGET already exists'); end if;
select count(*) into n from apex_workspaces where workspace='E3_TARGET';
if n>0 then raise_application_error(-20932,'E3 workspace already exists'); end if;
select count(*) into n from apex_applications where application_id=810203;
if n>0 then raise_application_error(-20933,'E3 application ID already exists'); end if;
end;
/""", admin=True)
    password = random.token_hex(20)
    c = {'sqlcl': str(ROOT / '.local-apex/tools/sqlcl-25.4.1.022.0618/sqlcl/bin/sql'),
         'java_home': str(ROOT / '.local-apex/tools/jdk-21.0.12.1+1/Contents/Home'),
         'sqlcl_home': str(ROOT / '.local-apex/tools/sqlcl-home-25.4.1-qualification'),
         'author_connection': 'lab-dev-c', 'service': '127.0.0.1:1521/FREEPDB1',
         'target_schema': 'E3_TARGET', 'target_app': 810203, 'target_password': password}
    config_file.write_text(json.dumps(c, indent=2)+'\n'); config_file.chmod(0o600)
    # No credential-bearing provisioning output is printed or retained as evidence.
    run(f'''create user E3_TARGET identified by "{password}" default tablespace USERS quota unlimited on USERS;
grant create session,create table,create view,create procedure,create trigger,create sequence,create type to E3_TARGET;
create table E3_TARGET.e3_lab_ownership(id varchar2(30) primary key);
insert into E3_TARGET.e3_lab_ownership values('E.3');
commit;
begin
apex_instance_admin.add_workspace(p_workspace=>'E3_TARGET',p_primary_schema=>'E3_TARGET');
apex_util.set_workspace('E3_TARGET');
apex_util.create_user(p_user_name=>'LAB_USER',p_web_password=>'{private['LAB_USER']}',p_email_address=>'e3@localhost',p_default_schema=>'E3_TARGET',p_developer_privs=>null,p_change_password_on_first_use=>'N');
commit;
end;
/''', admin=True)
    # Bundle retains the reviewed native baseline and its comparison history.
    # It contains source/configuration only, not runtime rows or credentials.
    subprocess.run(['git','clone','--branch','main',str(ROOT/'examples/git-pipeline/baseline.bundle'),str(REPO)],check=True)
    shutil.copytree(ROOT / 'examples/git-pipeline/scripts', REPO / 'scripts', dirs_exist_ok=True)
    def git(*args):
        return subprocess.check_output(['git','-C',str(REPO),*args],text=True).strip()
    for key in ['user.name','user.email']:
        git('config',key,subprocess.check_output(['git','-C',str(ROOT),'config',key],text=True).strip())
    git('remote','set-url','origin','https://github.com/rstyczynski/APEX_CICD_E3.git')
    print('Prepared new owned E3_TARGET / application 810203 and native project checkout.')
    print('E3_LAB_CONFIG='+str(config_file))


if __name__=='__main__':
    try:
        main()
    except ValueError as exc:
        print(str(exc),file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print('E.3 preparation stopped ('+type(exc).__name__+'); inspect the named resources and private configuration before retrying.',file=sys.stderr)
        sys.exit(1)
