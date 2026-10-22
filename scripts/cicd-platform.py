#!/usr/bin/env python3
"""Provision/check only the declared E.1 logical areas in the existing database."""
import json
import os
from pathlib import Path
import secrets as random_secrets
import sys
import subprocess

from apex_sql import LOCAL, ROOT, run
from cicd_environments import canonical, display
from cicd_config import load, identifier
import re

CONFIG = load(ROOT / 'config/areas.json')


def owned_inventory():
    users = [CONFIG['control_schema']] + [a['schema'] for a in CONFIG['areas'].values()]
    receipt = LOCAL / 'e1-owned.json'
    if receipt.exists():
        if json.loads(receipt.read_text()) != CONFIG:
            raise RuntimeError('Area configuration changed: inspect existing resources first.')
    else:
        names = ','.join("'" + u + "'" for u in users)
        apps = ','.join(str(a['application_id']) for a in CONFIG['areas'].values())
        run(f"""declare n number; begin
          select count(*) into n from dba_users where username in ({names});
          if n>0 then raise_application_error(-20001,'E.1 schema name collision'); end if;
          select count(*) into n from apex_workspaces where workspace in ({names});
          if n>0 then raise_application_error(-20002,'E.1 workspace name collision'); end if;
          select count(*) into n from apex_applications where application_id in ({apps});
          if n>0 then raise_application_error(-20003,'E.1 application ID collision'); end if;
        end;
        /""", admin=True)
        receipt.write_text(json.dumps(CONFIG, indent=2) + '\n')


def credentials(keys):
    path = LOCAL / 'e1-secrets.json'
    private = json.loads(path.read_text()) if path.exists() else {}
    for key in keys:
        private.setdefault(key, 'Ee1_' + random_secrets.token_hex(18))
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    os.fchmod(fd, 0o600)
    with os.fdopen(fd, 'w') as f:
        json.dump(private, f)
    return private


def create_schema(user, private):
    identifier(user)
    if not isinstance(private.get(user), str) or not re.fullmatch(r'[A-Za-z0-9_#]+', private[user]):
        raise ValueError('Unsafe lab schema password')
    run(f"""declare n number; begin
      select count(*) into n from dba_users where username='{user}';
      if n=0 then
        execute immediate 'create user {user} identified by "{private[user]}" default tablespace USERS quota 128M on USERS';
        execute immediate 'grant create session, create table, create view, create procedure, create sequence, create trigger to {user}';
      end if;
    end;
    /""", admin=True)


def control_identity():
    owned_inventory()
    user=CONFIG['control_schema']
    private=credentials([user])
    create_schema(user,private)
    run('select user from dual;',save=('lab-control',user,user))
    print('Provisioned control identity only: '+user)


def provision(name):
    name = canonical(name)
    if name not in CONFIG['areas']: raise ValueError('Select one declared area')
    owned_inventory()
    run("declare n number; begin select count(*) into n from dba_objects where owner='E1_CTRL' and object_name in ('E1_OWNERSHIP','E1_RELEASE') and object_type='PACKAGE BODY' and status='VALID'; if n<>2 then raise_application_error(-20810,'Initialize project control first'); end if; end;\n/",admin=True)
    area=CONFIG['areas'][name]
    developer={'lab-dev':'DEV_A','lab-dev-b':'DEV_B','lab-dev-c':'DEV_C'}.get(name)
    keys=[area['schema'],'LAB_USER','VERIFIER']+([developer] if developer else [])
    private=credentials(keys)
    create_schema(area['schema'],private)
    user = area['schema']
    create_developer = ''
    if developer:
        create_developer = f"""if not apex_util.is_username_unique('{developer}') then null; else
          apex_util.create_user(p_user_name=>'{developer}',p_web_password=>'{private[developer]}',
            p_email_address=>'developer@localhost',p_default_schema=>'{user}',
            p_developer_privs=>'ADMIN:CREATE:DATA_LOADER:EDIT:HELP:MONITOR:SQL',
            p_change_password_on_first_use=>'N'); end if;"""
    run(f"""declare n number; begin
      select count(*) into n from apex_workspaces where workspace='{area['workspace']}';
      if n=0 then apex_instance_admin.add_workspace(p_workspace=>'{area['workspace']}',p_primary_schema=>'{user}'); end if;
      apex_util.set_workspace(p_workspace=>'{area['workspace']}');
      {create_developer}
      if apex_util.is_username_unique('LAB_USER') then
        apex_util.create_user(p_user_name=>'LAB_USER',p_web_password=>'{private['LAB_USER']}',
          p_email_address=>'lab@localhost',p_default_schema=>'{user}',p_developer_privs=>null,
          p_change_password_on_first_use=>'N',p_allow_app_building_yn=>'N',p_allow_sql_workshop_yn=>'N');
      end if;
      if apex_util.is_username_unique('VERIFIER') then
        apex_util.create_user(p_user_name=>'VERIFIER',p_web_password=>'{private['VERIFIER']}',
          p_email_address=>'verify@localhost',p_default_schema=>'{user}',p_developer_privs=>null,
          p_change_password_on_first_use=>'N',p_allow_app_building_yn=>'N',p_allow_sql_workshop_yn=>'N');
      end if;
      commit;
    end;
    /""", admin=True)
    run('select user from dual;', save=(name, user, user))
    print(f'Provisioned ONLY {display(name)}: {user} / {area["workspace"]}')
    grants=f"grant execute on E1_CTRL.e1_release to {user};\n"
    if developer: grants+=f"grant execute on E1_CTRL.e1_ownership to {user};\n"
    run(grants,admin=True)
    print('Granted only this area its delivery interfaces; other areas unchanged.')

def check():
    for name in CONFIG['areas']:
        subprocess.run([sys.executable,str(ROOT/'scripts/cicd-isolation.py'),'identity',name],check=True)


def isolation():
    subprocess.run([sys.executable,str(ROOT/'scripts/cicd-isolation.py'),'all'],check=True)


def reset_qualification():
    receipt = LOCAL / 'e1-owned.json'
    if not receipt.exists() or json.loads(receipt.read_text()) != CONFIG:
        raise RuntimeError('No matching owned-area inventory')
    area = CONFIG['areas']['integration_test']
    # Only the explicitly disposable integration_test area is a reset target.
    run(f"""begin
      apex_instance_admin.remove_workspace(p_workspace=>'{area['workspace']}',p_drop_users=>'Y',p_drop_tablespaces=>'N');
    end;
    /""", admin=True)
    provision('integration_test')
    print('Disposable integration_test area recreated; other areas retained.')


def preservation_check():
    run("""begin
      begin insert into e1_private_probe values (1001); exception when dup_val_on_index then null; end;
      commit;
    end;
    /""", connection='user_acceptance_test')
    assertion = """declare n number; begin
      select count(*) into n from e1_private_probe where id=1001;
      if n<>1 then raise_application_error(-20030,'Retained TEST marker missing'); end if;
    end;
    /"""
    run(assertion, connection='user_acceptance_test')
    reset_qualification()
    run(assertion, connection='user_acceptance_test')
    try:
        run("begin raise_application_error(-20031,'Expected failure propagation check'); end;\n/", connection='user_acceptance_test')
    except RuntimeError:
        print('PASS: Oracle failure propagates as failure.')
    else:
        raise RuntimeError('Oracle failure incorrectly reported success')
    print('PASS: committed TEST marker survived integration_test-area recreation.')


if __name__ == '__main__':
    try:
        if sys.argv[1:] == ['control-identity']:
            control_identity()
        elif len(sys.argv)==3 and sys.argv[1]=='provision':
            provision(sys.argv[2])
        elif sys.argv[1:] == ['check-empty']:
            print(run((ROOT/'deploy/operator/walkthrough_empty.sql').read_text(),admin=True))
        elif sys.argv[1:] == ['check']:
            check()
        elif sys.argv[1:] == ['isolation']:
            isolation()
        elif sys.argv[1:] in (['reset-integration-test'], ['reset-qualify']):
            reset_qualification()
        elif sys.argv[1:] == ['preservation-check']:
            preservation_check()
        else:
            raise ValueError('Usage: cicd-platform.py control-identity|provision TARGET|check|check-empty|isolation|reset-integration-test|preservation-check')
    except (ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)
