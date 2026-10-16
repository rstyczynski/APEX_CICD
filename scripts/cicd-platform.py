#!/usr/bin/env python3
"""Provision/check only the declared E.1 logical areas in the existing database."""
import json
import os
from pathlib import Path
import secrets as random_secrets
import sys

from apex_sql import LOCAL, ROOT, run

CONFIG = json.loads((ROOT / 'config/areas.json').read_text())


def bootstrap():
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
    path = LOCAL / 'e1-secrets.json'
    private = json.loads(path.read_text()) if path.exists() else {}
    for key in users + ['DEV_A', 'DEV_B', 'DEV_C', 'LAB_USER', 'VERIFIER']:
        private.setdefault(key, 'Ee1_' + random_secrets.token_hex(18))
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, 'w') as f:
        json.dump(private, f)
    for user in users:
        run(f"""declare n number; begin
          select count(*) into n from dba_users where username='{user}';
          if n=0 then
            execute immediate 'create user {user} identified by "{private[user]}" default tablespace USERS quota 128M on USERS';
            execute immediate 'grant create session, create table, create view, create procedure, create sequence, create trigger to {user}';
          end if;
        end;
        /""", admin=True)
    for index, (name, area) in enumerate(CONFIG['areas'].items()):
        user = area['schema']
        developer = ['DEV_A', 'DEV_B', 'DEV_C', None, None][index]
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
        print(f'Provisioned {name}: {user} / {area["workspace"]}')
    run('select user from dual;', save=('lab-control', CONFIG['control_schema'], CONFIG['control_schema']))


def check():
    for name, area in CONFIG['areas'].items():
        run(f"""declare n number; begin
          if user<>'{area['schema']}' or sys_context('USERENV','CON_NAME')<>'FREEPDB1' then
            raise_application_error(-20010,'Wrong effective target'); end if;
          select count(*) into n from apex_workspace_schemas where workspace_name='{area['workspace']}' and schema='{area['schema']}';
          if n<>1 then raise_application_error(-20011,'Wrong workspace/schema association'); end if;
        end;
        /""", connection=name)
        print(f'PASS {name}: effective schema/PDB/workspace mapping')


def isolation():
    for name, area in CONFIG['areas'].items():
        run("""declare n number; begin
          select count(*) into n from user_tables where table_name='E1_PRIVATE_PROBE';
          if n=0 then execute immediate 'create table e1_private_probe (id number primary key)'; end if;
        end;
        /""", connection=name)
    names = list(CONFIG['areas'])
    for index, name in enumerate(names):
        foreign = CONFIG['areas'][names[(index+1) % len(names)]]['schema']
        run(f"""declare n number; begin
          begin
            execute immediate 'select count(*) from {foreign}.e1_private_probe' into n;
            raise_application_error(-20020,'Cross-area read was permitted');
          exception when others then if sqlcode not in (-942,-1031) then raise; end if; end;
          begin
            execute immediate 'insert into {foreign}.e1_private_probe values (1)';
            rollback;
            raise_application_error(-20021,'Cross-area write was permitted');
          exception when others then if sqlcode not in (-942,-1031) then raise; end if; end;
        end;
        /""", connection=name)
        print(f'PASS {name}: cross-area read/write denied')


def reset_qualification():
    receipt = LOCAL / 'e1-owned.json'
    if not receipt.exists() or json.loads(receipt.read_text()) != CONFIG:
        raise RuntimeError('No matching owned-area inventory')
    area = CONFIG['areas']['lab-qualify']
    # Only the explicitly disposable qualification area is a reset target.
    run(f"""begin
      apex_instance_admin.remove_workspace(p_workspace=>'{area['workspace']}',p_drop_users=>'Y',p_drop_tablespaces=>'N');
    end;
    /""", admin=True)
    bootstrap()
    print('Disposable qualification area recreated; other areas retained.')


def preservation_check():
    run("""begin
      begin insert into e1_private_probe values (1001); exception when dup_val_on_index then null; end;
      commit;
    end;
    /""", connection='lab-test')
    assertion = """declare n number; begin
      select count(*) into n from e1_private_probe where id=1001;
      if n<>1 then raise_application_error(-20030,'Retained TEST marker missing'); end if;
    end;
    /"""
    run(assertion, connection='lab-test')
    reset_qualification()
    run(assertion, connection='lab-test')
    try:
        run("begin raise_application_error(-20031,'Expected failure propagation check'); end;\n/", connection='lab-test')
    except RuntimeError:
        print('PASS: Oracle failure propagates as failure.')
    else:
        raise RuntimeError('Oracle failure incorrectly reported success')
    print('PASS: committed TEST marker survived qualification-area recreation.')


if __name__ == '__main__':
    try:
        if sys.argv[1:] == ['bootstrap']:
            bootstrap()
        elif sys.argv[1:] == ['check']:
            check()
        elif sys.argv[1:] == ['isolation']:
            isolation()
        elif sys.argv[1:] == ['reset-qualify']:
            reset_qualification()
        elif sys.argv[1:] == ['preservation-check']:
            preservation_check()
        else:
            raise ValueError('Usage: cicd-platform.py bootstrap|check|isolation|reset-qualify|preservation-check')
    except (ValueError, RuntimeError) as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)
