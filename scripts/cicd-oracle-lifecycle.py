#!/usr/bin/env python3
"""Disposable E.2 utilities; section scripts own the workflow, not this module."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import secrets
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
from apex_sql import command as sql_command, run as admin_sql, secrets as platform_secrets

BASE = ROOT / '.local-apex/e2'
SQL_FIXTURES = ROOT / 'tests/sql/oracle_lifecycle'
ERRORS = re.compile(r'(?im)^\s*(?:ORA-\d{5}:|PLS-\d{5}:|SP2-\d+:|ERROR\b|Errors:\s*[1-9]\d*|Error starting|Unknown Command|SEVERE:)|Option not recognized|Option not found|No database connection|Unable to render the settings|java\.[\w.]+Exception|The option .+ is required')


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, value, private=False):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + '.tmp')
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')
    tmp.chmod(0o600 if private else 0o644)
    tmp.replace(path)


def write_receipt(path, value):
    path = Path(path)
    if path.exists():
        retained = path.parent / 'attempts' / (now().replace(':', '-') + '-' + path.name)
        retained.parent.mkdir(exist_ok=True)
        retained.write_bytes(path.read_bytes())
    write_json(path, value)


def load(run):
    if not re.fullmatch(r'[a-z][a-z0-9-]{2,40}', run):
        raise ValueError('Run ID must be 3-41 lowercase letters/digits/hyphens')
    path = BASE / run
    return path, json.loads((path / 'inventory.json').read_text())


def config_service():
    service = json.loads((ROOT / 'config/areas.json').read_text())['service']
    if service != '127.0.0.1:1521/FREEPDB1':
        raise ValueError('This approved exercise is bound to the loopback FREEPDB1 lab')
    return service


def redact(output, private=None):
    values = list(platform_secrets().values())
    if private:
        values.extend(private.values())
    for value in sorted((v for v in values if isinstance(v, str) and v), key=len, reverse=True):
        output = output.replace(value, '[REDACTED]')
    return output


def identity():
    out = admin_sql("set heading off pagesize 0\nselect 'E2_ID|'||dbid||'|'||name from v$database;\nselect 'E2_PDB|'||sys_context('USERENV','CON_NAME') from dual;\nselect 'E2_APEX|'||version_no from apex_release;\nselect 'E2_DB|'||version_full from v$instance;", admin=True)
    data = {}
    for line in out.splitlines():
        line = line.strip()
        if line.startswith('E2_') and '|' in line:
            key, value = line.split('|', 1)
            data[key] = value
    if data.get('E2_PDB') != 'FREEPDB1' or not data.get('E2_APEX', '').startswith('24.2.'):
        raise ValueError('Unexpected PDB/APEX identity: ' + json.dumps(data))
    if not data.get('E2_DB', '').startswith('23.26.'):
        raise ValueError('Unexpected Database version: ' + json.dumps(data))
    return data


def sql(run, role, body, cwd=None, offline=False):
    path, inv = load(run)
    private = json.loads((path / 'private.json').read_text())
    prefix = 'set echo off verify off define off serveroutput on\nwhenever oserror exit failure rollback\nwhenever sqlerror exit failure rollback\n'
    if not offline:
        if role not in inv['roles']:
            raise ValueError('Foreign role rejected')
        current = identity()
        if inv.get('identity') != current:
            raise ValueError('DB/PDB identity changed; refuse operation')
        schema = inv['roles'][role]['schema']
        prefix += f'connect {schema}/"{private[role]}"@//{config_service()}\n'
    marker = 'E2_CLIENT_COMPLETE' if offline else 'E2_SERVER_COMPLETE'
    end = f'prompt {marker}\n' if offline else f"begin dbms_output.put_line('{marker}'); end;\n/\n"
    env = os.environ.copy()
    env['JAVA_HOME'] = str(ROOT / '.local-apex/tools/jdk-21.0.12.1+1/Contents/Home')
    env.pop('JAVA_TOOL_OPTIONS', None)
    result = subprocess.run(sql_command(), input=prefix + body + '\n' + end + 'exit success\n',
                            cwd=cwd or path / 'repo', env=env, text=True, capture_output=True, timeout=300)
    output = redact(result.stdout + result.stderr, private)
    log = path / 'logs' / (datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f') + '.log')
    log.parent.mkdir(exist_ok=True)
    log.write_text(output)
    if result.returncode or ERRORS.search(output) or not re.search(r'(?m)^' + marker + r'\s*$', output):
        raise RuntimeError(f'SQLcl operation failed; evidence {log.relative_to(ROOT)}\n{output[-5000:]}')
    return re.sub(r'(?m)^' + marker + r'\s*$', '', output).strip()


def guard(run, role):
    path, inv = load(run)
    if role not in inv['roles']:
        raise ValueError('Foreign role refused before connection')
    output = sql(run, role, "select 'E2_OWNER|'||run_id from e2_run_ownership;")
    if 'E2_OWNER|' + run not in output:
        raise ValueError('Ownership marker mismatch')
    return path, inv


def git(path, *args):
    return subprocess.check_output(['git', *args], cwd=path, text=True).strip()


def declaration_path(path):
    native = path / 'repo/dist/component-contract.json'
    legacy = path / 'repo/component-contract.json'
    if native.exists() and legacy.exists():
        raise ValueError('Two declaration authorities exist; reconcile before capture/deployment')
    return native if native.exists() else legacy


def init(run):
    if not re.fullmatch(r'[a-z][a-z0-9-]{2,40}', run):
        raise ValueError('Invalid run ID')
    path = BASE / run
    partial_local = path.exists()
    if partial_local:
        _, old = load(run)
        if old.get('identity') or old.get('empty_base_commit'):
            raise ValueError('Run already initialized or provisioned; never overwrite it')
        if not (path / 'private.json').is_file():
            raise ValueError('Incomplete local ownership; inspect before recovery')
    else:
        path.mkdir(parents=True, mode=0o700)
    repo = path / 'repo'
    repo.mkdir(exist_ok=partial_local)
    suffix = hashlib.sha256(run.encode()).hexdigest()[:8].upper()
    roles = {r: {'schema': f'E2_{suffix}_{letter}', 'workspace': f'E2_{suffix}_{letter}',
                 'application_id': 820000 + int(suffix[:4], 16) * 3 + i,
                 'offset': 1000000000000 + int(suffix, 16) * 1000000 + i * 100000}
             for i, (r, letter) in enumerate([('author', 'A'), ('fresh', 'F'), ('upgrade', 'U')])}
    inv = {'format': 1, 'run_id': run, 'created_at': now(), 'service': config_service(),
           'source_commit': git(ROOT, 'rev-parse', 'HEAD'), 'roles': roles, 'identity': None}
    private = {r: secrets.token_hex(18) for r in roles}
    private['developer'] = secrets.token_hex(18)
    if partial_local:
        inv = old
    else:
        write_json(path / 'inventory.json', inv)
        write_json(path / 'private.json', private, True)
    if not (repo / '.git').exists():
        git(repo, 'init', '-b', 'codex/e2-base')
    git(repo, 'config', 'user.name', git(ROOT, 'config', 'user.name') or 'APEX laboratory')
    git(repo, 'config', 'user.email', git(ROOT, 'config', 'user.email') or 'lab@localhost')
    if not (repo / '.dbtools/project.config.json').exists():
        print(sql(run, 'author', f'project init -name e2 -schemas {roles["author"]["schema"]}', offline=True))
    cfg_path = repo / '.dbtools/project.config.json'
    cfg = json.loads(cfg_path.read_text())
    cfg['export']['setTransform']['emitSchema'] = False
    cfg['export']['apex']['expOriginalIds'] = True
    cfg['git']['defaultBranch'] = 'codex/e2-base'
    write_json(cfg_path, cfg)
    initial = json.loads((ROOT / 'release/manifest.json').read_text())
    initial['release'] = '1.0.0'
    initial['stage'] = 'complete-initial'
    initial['components']['Hello'] = '1.0.0'
    initial['supported_starts'] = ['empty']
    initial.pop('base_artifact', None)
    for key in ('native_import_status', 'publication_profile', 'runtime_gate', 'capture_profile', 'fingerprint_profile'):
        initial.pop(key, None)
    initial['delivery_profile'] = 'E2-native-PROJECT-under-assessment'
    write_json(repo / 'dist/component-contract.json', initial)
    git(repo, 'add', '.')
    git(repo, 'commit', '-m', 'chore: initialize native PROJECT and explicit component declaration')
    inv['empty_base_commit'] = git(repo, 'rev-parse', 'HEAD')
    git(repo, 'tag', 'e2-empty-base')
    git(repo, 'branch', 'e2-empty-base', inv['empty_base_commit'])
    write_json(path / 'inventory.json', inv)
    print('CREATED ' + str(path.relative_to(ROOT)))


def preflight(run=None):
    checks = {'service': config_service(), 'sqlcl': str(ROOT / '.local-apex/tools/sqlcl/bin/sql')}
    if run and (BASE / run / 'inventory.json').exists():
        path, inv = load(run)
        checks['run'] = run
        checks['repo_head'] = git(path / 'repo', 'rev-parse', 'HEAD')
    checks['runtime'] = identity()
    checks['scheduler_capacity'] = admin_sql("""select 'PDB_JOB_WORKERS|'||value from v$parameter where name='job_queue_processes';
alter session set container=CDB$ROOT;
select 'CDB_JOB_WORKERS|'||value from v$parameter where name='job_queue_processes';
alter session set container=FREEPDB1;""", admin=True).strip()
    print(json.dumps(checks, indent=2))


def provision(run):
    path, inv = load(run)
    private = json.loads((path / 'private.json').read_text())
    current = identity()
    if inv['identity'] and inv['identity'] != current:
        raise ValueError('Refuse to reuse run on a different database')
    if not inv['identity']:
        names = ','.join("'" + r['schema'] + "'" for r in inv['roles'].values())
        apps = ','.join(str(r['application_id']) for r in inv['roles'].values())
        admin_sql(f"declare n number; begin select count(*) into n from dba_users where username in ({names}); if n>0 then raise_application_error(-20901,'E2 schema collision'); end if; select count(*) into n from apex_workspaces where workspace in ({names}); if n>0 then raise_application_error(-20902,'E2 workspace collision'); end if; select count(*) into n from apex_applications where application_id in ({apps}); if n>0 then raise_application_error(-20903,'E2 app ID collision'); end if; end;\n/", admin=True)
        inv['identity'] = current
        inv['allocation_started_at'] = now()
        write_json(path / 'inventory.json', inv)
    for role, entry in inv['roles'].items():
        user = entry['schema']
        try:
            count = admin_sql(f"select 'E2_EXISTS|'||count(*) from dba_users where username='{user}';", admin=True)
            if 'E2_EXISTS|1' in count:
                guard(run, role)
                print('VERIFIED existing owned ' + user)
                continue
            body = f'''create user {user} identified by "{private[role]}" default tablespace USERS quota unlimited on USERS;
 grant create session,create table,create view,create procedure,create trigger,create sequence,create type to {user};
 create table {user}.e2_run_ownership(run_id varchar2(41) primary key);
 insert into {user}.e2_run_ownership values('{run}');
 commit;
 begin
 apex_instance_admin.add_workspace(p_workspace=>'{entry['workspace']}',p_primary_schema=>'{user}');
 apex_util.set_workspace(p_workspace=>'{entry['workspace']}');
 apex_util.create_user(p_user_name=>'E2DEV',p_web_password=>'{private['developer']}',p_email_address=>'e2@localhost',p_default_schema=>'{user}',p_developer_privs=>'ADMIN:CREATE:DATA_LOADER:EDIT:HELP:MONITOR:SQL',p_change_password_on_first_use=>'N');
 commit;
 end;
 /'''
            print(redact(admin_sql(body, admin=True), private))
            guard(run, role)
        except Exception:
            raise RuntimeError('Partial provisioning: inspect this run; no blind recreation of ' + user)
    print('OWNED RESOURCES READY; author workspace=' + inv['roles']['author']['workspace'])


def fixture(run):
    path, inv = guard(run, 'author')
    output = sql(run, 'author', "select 'E2_FIXTURE|'||count(*) from user_tables where table_name='E2_COMPONENTS';")
    if 'E2_FIXTURE|0' in output:
        print(sql(run, 'author', f'@"{SQL_FIXTURES / "fixture.sql"}"\n@"{SQL_FIXTURES / "seed.sql"}"'))
    elif 'E2_FIXTURE|1' not in output:
        raise ValueError('Unknown fixture state')
    print(snapshot(run, 'author'))


def app(run, app_id):
    path, inv = guard(run, 'author')
    app_id = int(app_id)
    schema = inv['roles']['author']['schema']
    output = sql(run, 'author', f"select 'E2_APP|'||application_id from apex_applications where application_id={app_id} and owner='{schema}' and workspace='{schema}';")
    if f'E2_APP|{app_id}' not in output:
        raise ValueError('App is not in this run author workspace/schema')
    inv['roles']['author']['application_id'] = app_id
    write_json(path / 'inventory.json', inv)
    filters = path / 'repo/.dbtools/filters/project.filters'
    data = filters.read_text()
    mark = '\n-- E2 owned scope\n'
    data = data.split(mark)[0].rstrip().rstrip(',')
    data += f",{mark}object_name not like 'E2_RUN_%',\nexport_type != 'ORDS_SCHEMA',\n(export_type != 'APEX_APPLICATIONS' or application_id = {app_id})\n"
    filters.write_text(data)
    print('ADOPTED owned Main application ' + str(app_id))


def snapshot(run, role):
    path, inv = guard(run, role)
    return sql(run, role, """set heading off pagesize 0 linesize 32767
select 'COMPONENT|'||component||'|'||version from e2_components order by component;
select 'SETTING|'||setting_key||'|'||setting_value from e2_settings order by setting_key;
select 'HISTORY|'||history_id||'|'||greeting_text||'|'||to_char(recorded_at,'YYYY-MM-DD HH24:MI:SS.FF6') from e2_history order by history_id;
select 'GREETING|'||e2_greeting.greeting from dual;
declare n number; c sys_refcursor; k varchar2(60); v varchar2(50); begin
select count(*) into n from user_tab_columns where table_name='E2_SETTINGS' and column_name='RELEASE_NOTE';
if n=1 then
open c for 'select setting_key,release_note from e2_settings order by setting_key';
loop fetch c into k,v; exit when c%notfound; dbms_output.put_line('SETTING_NOTE|'||k||'|'||nvl(v,'<NULL>')); end loop;
close c;
end if;
end;
/
""")


def project(run, action, value=None):
    path, inv = guard(run, 'author')
    repo = path / 'repo'
    if action == 'export':
        app_id = inv['roles']['author']['application_id']
        # Export is always scope-filtered; list and actual output are retained.
        print(sql(run, 'author', 'project export -list'))
        print(sql(run, 'author', 'project export'))
        if not list((repo / 'src').rglob('*.sql')):
            raise ValueError('No importable source files captured')
        for f in (repo / 'src').rglob('*'):
            if f.is_file() and ('E2_RUN_OWNERSHIP' in f.name.upper()):
                raise ValueError('Ownership fixture leaked into capture')
        print('REVIEW diff and inventory; expected Main=' + str(app_id))
        print(git(repo, 'status', '--short'))
    elif action == 'commit':
        git(repo, 'add', '.')
        if git(repo, 'status', '--porcelain'):
            print(git(repo, 'commit', '-m', value or 'feat: reviewed E2 source checkpoint'))
        print('SOURCE ' + git(repo, 'rev-parse', 'HEAD'))
    elif action == 'stage':
        base = value or inv['empty_base_commit']
        if not re.fullmatch(r'[A-Za-z0-9_./-]+', base):
            raise ValueError('Unsafe comparison base')
        git(repo, 'rev-parse', '--verify', 'refs/heads/' + base)
        print(sql(run, 'author', 'project stage -branch-name ' + base))
        inv['stage_base_branch'] = base
        write_json(path / 'inventory.json', inv)
    elif action == 'custom':
        if value not in ('seed', 'patch'):
            raise ValueError('Select intentional seed or patch SQL')
        name = 'e2_' + value + '.sql'
        print(sql(run, 'author', 'project stage add-custom -file-name ' + name))
        matches = list((repo / 'dist').rglob(name))
        if len(matches) != 1:
            raise ValueError('Expected exactly one generated custom changeset')
        custom = matches[0]
        original = custom.read_text()
        if 'E2_INTENTIONAL_DATA' not in original:
            custom.write_text(original + '\n-- E2_INTENTIONAL_DATA\n' + (SQL_FIXTURES / (value + '.sql')).read_text())
        print('REVIEW CUSTOM ' + str(custom.relative_to(repo)))
    elif action == 'release':
        if not re.fullmatch(r'1\.0\.[01]', value or ''):
            raise ValueError('Only the bounded initial/patch releases are supported')
        print(sql(run, 'author', 'project verify -compared-branch-name ' + inv.get('stage_base_branch', 'e2-empty-base')))
        print(sql(run, 'author', 'project release -version ' + value))
    elif action == 'verify':
        print(sql(run, 'author', 'project verify -compared-branch-name ' + (value or inv.get('stage_base_branch', 'e2-empty-base')) + ' -verbose'))
    elif action == 'mapping-hook':
        file = repo / 'dist/install.sql'
        text = file.read_text()
        command = 'lb update -log -changelog-file releases/main.changelog.xml -search-path "."'
        if '-defaults-file &DEFAULTS_FILE' not in text:
            if command not in text:
                raise ValueError('Generated installer differs; inspect mapping hook manually')
            text = text.replace(command, command + ' -defaults-file &DEFAULTS_FILE')
        file.write_text(text.replace('set define off', 'set define on'))
        print('REVIEW Oracle paper page 30 mapping hook; property file remains target-specific')
    elif action == 'artifact':
        if not re.fullmatch(r'[A-Za-z0-9.-]+', value or ''):
            raise ValueError('Invalid artifact label')
        print(sql(run, 'author', f'project gen-artifact -name e2 -version {value} -format zip'))
        files = list((repo / 'artifact').glob('*.zip'))
        if not files:
            raise ValueError('Native artifact not found')
        for f in files:
            print('ARTIFACT ' + str(f.relative_to(path)) + ' SHA256 ' + digest(f))
    else:
        raise ValueError('Unsupported PROJECT action')


def deploy(run, role, artifact):
    path, inv = guard(run, role)
    if role == 'author':
        raise ValueError('Never deploy release artifacts over authoring')
    archive = Path(artifact).resolve()
    if not archive.is_relative_to((path / 'repo/artifact').resolve()) or archive.suffix != '.zip':
        raise ValueError('Only this run native artifacts may be deployed')
    declaration = json.loads(declaration_path(path).read_text())
    validate_contract(declaration)
    admit(run, role, archive)
    if role == 'upgrade':
        qualification = json.loads((path / 'qualification.json').read_text())
        for key, value in {'artifact_sha256': digest(archive),
                           'source_commit': source_binding(path),
                           'declaration_sha256': digest(declaration_path(path))}.items():
            if qualification.get(key) != value:
                raise ValueError('Qualification does not match candidate ' + key)
    entry = inv['roles'][role]
    app_id = inv['roles']['author']['application_id']
    # The generated APEX changeset clears session setters. Use the paper's
    # properties/defaults-file hook, with exact property spelling from this client.
    properties = path / f'deploy-{role}.properties'
    alias = f'E2-{role.upper()}-{entry["application_id"]}'
    properties.write_text(f'apex.{app_id}.workspace:{entry["workspace"]}\napex.{app_id}.appId:{entry["application_id"]}\napex.{app_id}.schema:{entry["schema"]}\napex.{app_id}.alias:{alias}\n')
    with zipfile.ZipFile(archive) as z:
        installers = [name for name in z.namelist() if name == 'install.sql' or name.endswith('/dist/install.sql')]
        if len(installers) != 1:
            raise ValueError('Expected one native installer')
        installer = z.read(installers[0]).decode()
        if '-defaults-file &DEFAULTS_FILE' not in installer or 'set define on' not in installer:
            raise ValueError('Native artifact lacks reviewed mapping hook; refuse default author identity')
        if 'component-contract.json' in z.namelist():
            if hashlib.sha256(z.read('component-contract.json')).hexdigest() != digest(declaration_path(path)):
                raise ValueError('Native embedded declaration differs from reviewed declaration')
            print('NATIVE ARCHIVE carries the exact reviewed declaration; semantic admission remains explicit')
        else:
            print('ASSESSMENT LIMIT: this earlier candidate uses an external bound declaration')
    body = f"""set define on
define DEFAULTS_FILE="{properties}"
project deploy -file "{archive}"
"""
    print(sql(run, role, body))
    print('DEPLOYED SHA256 ' + digest(archive))
    print(snapshot(run, role))
    after = target_state(run, role)
    expected = declaration['components']
    observed = {line.split('|')[1]: line.split('|')[2] for line in after.splitlines()
                if line.startswith('COMPONENT|')}
    if observed != expected:
        raise ValueError('Installed component versions differ from declaration')
    write_receipt(path / f'deployed-{role}.json', {
        'at': now(), 'artifact_sha256': digest(archive), 'state': after,
        'state_sha256': hashlib.sha256(after.encode()).hexdigest()})


def target_state(run, role):
    path, inv = guard(run, role)
    output = sql(run, role, "select 'E2_PRESENT|'||count(*) from user_tables where table_name='E2_COMPONENTS';")
    if 'E2_PRESENT|0' in output:
        app_id = inv['roles'][role]['application_id']
        empty = sql(run, role, f"""select 'E2_LEFTOVERS|'||count(*) from user_objects
where object_type in ('TABLE','VIEW','PACKAGE','PACKAGE BODY','PROCEDURE','FUNCTION','TRIGGER','SEQUENCE')
and object_name!='E2_RUN_OWNERSHIP';
select 'E2_EXISTING_APP|'||count(*) from apex_applications where application_id={app_id};""")
        if 'E2_LEFTOVERS|0' not in empty or 'E2_EXISTING_APP|0' not in empty:
            raise ValueError('Partial/unknown target is not empty; inspect before any retry')
        return 'EMPTY'
    if 'E2_PRESENT|1' not in output:
        raise ValueError('Unknown installed state')
    state = '\n'.join(line.strip() for line in snapshot(run, role).splitlines()
                      if line.strip().startswith(('COMPONENT|', 'SETTING|', 'SETTING_NOTE|', 'HISTORY|', 'GREETING|')))
    app_id = inv['roles'][role]['application_id']
    definitions = sql(run, role, f"""set heading off pagesize 0 linesize 32767
select 'DEF|'||table_name||'|'||column_id||'|'||column_name||'|'||data_type||'|'||data_length||'|'||nullable
from user_tab_columns where table_name in ('E2_COMPONENTS','E2_SETTINGS','E2_HISTORY') order by table_name,column_id;
select 'CODE|'||name||'|'||type||'|'||line||'|'||text from user_source where name='E2_GREETING' order by type,line;
declare f apex_t_export_files; n number; begin
select count(*) into n from apex_applications where application_id={app_id};
if n=1 then
f:=apex_export.get_application(p_application_id=>{app_id},p_type=>'CHECKSUM-SH256',p_with_date=>false,p_with_original_ids=>true,p_with_supporting_objects=>'N',p_with_audit_info=>null);
for i in 1..f.count loop dbms_output.put_line('APEX|'||dbms_lob.substr(f(i).contents,32700,1)); end loop;
else dbms_output.put_line('APEX|ABSENT'); end if;
end;
/
""")
    # This is bounded fixture drift coverage, not full E.1 fencing/recovery.
    relevant = '\n'.join(x.strip() for x in definitions.splitlines()
                         if x.strip().startswith(('DEF|','CODE|','APEX|')))
    return state + '\nDEFINITIONS|' + hashlib.sha256(relevant.encode()).hexdigest()


def source_binding(path):
    repo = path / 'repo'
    if git(repo, 'status', '--porcelain'):
        raise ValueError('Uncommitted native source/distribution; review and commit first')
    return git(repo, 'rev-parse', 'HEAD')


def bind(run, role, artifact):
    path, inv = guard(run, role)
    if role == 'author':
        raise ValueError('Authoring is not a release target')
    archive = Path(artifact).resolve()
    if not archive.is_relative_to((path / 'repo/artifact').resolve()) or not archive.is_file():
        raise ValueError('Foreign artifact refused')
    declaration_file = declaration_path(path)
    contract = json.loads(declaration_file.read_text())
    validate_contract(contract)
    state = target_state(run, role)
    allowed = contract['supported_starts']
    if state == 'EMPTY' and 'empty' not in allowed:
        raise ValueError('Empty starting target not declared supported')
    if state != 'EMPTY':
        current = dict((line.split('|')[1], line.split('|')[2]) for line in state.splitlines()
                       if line.startswith('COMPONENT|'))
        if current not in [dict(Foundation='1.0.0', Hello='1.0.0', World='1.0.0'),
                           dict(Foundation='1.0.0', Hello='1.0.1', World='1.0.0')]:
            raise ValueError('Unknown installed component combination')
        # Exact initial-to-patch and repeat are the bounded supported starts.
        if current != contract['components'] and '1.0.0' not in allowed:
            raise ValueError('Installed starting state is not supported')
    receipt = {'run_id': run, 'role': role, 'at': now(), 'identity': identity(),
               'target': inv['roles'][role], 'source_commit': source_binding(path),
               'artifact_sha256': digest(archive), 'declaration_sha256': digest(declaration_file),
               'state_sha256': hashlib.sha256(state.encode()).hexdigest(),
               'validation': 'explicit-declarations-and-observed-start; runtime qualification separate'}
    destination = path / f'admission-{role}.json'
    if destination.exists():
        saved = path / 'attempts' / (now().replace(':', '-') + '-' + destination.name)
        saved.parent.mkdir(exist_ok=True)
        saved.write_bytes(destination.read_bytes())
    write_json(destination, receipt)
    print('BOUND ' + str(destination.relative_to(ROOT)))


def admit(run, role, artifact):
    path, inv = guard(run, role)
    receipt = json.loads((path / f'admission-{role}.json').read_text())
    current = {'run_id': run, 'role': role, 'identity': identity(),
               'target': inv['roles'][role], 'source_commit': source_binding(path),
               'artifact_sha256': digest(artifact),
               'declaration_sha256': digest(declaration_path(path)),
               'state_sha256': hashlib.sha256(target_state(run, role).encode()).hexdigest()}
    for key, value in current.items():
        if receipt.get(key) != value:
            raise ValueError('STALE ADMISSION ' + key + '; no deploy invoked')
    validate_contract(json.loads(declaration_path(path).read_text()))
    print('ADMITTED explicit declaration and exact observed target; native runtime protections unqualified')


def qualify(run, artifact):
    path, inv = guard(run, 'fresh')
    receipt = json.loads((path / 'deployed-fresh.json').read_text())
    if receipt['artifact_sha256'] != digest(artifact):
        raise ValueError('Fresh qualification refers to other artifact bytes')
    state = target_state(run, 'fresh')
    if 'GREETING|Hello World' not in state:
        raise ValueError('Greeting functional result missing')
    output = sql(run, 'fresh', f"select 'E2_INSTALLED_APP|'||application_id from apex_applications where application_id={inv['roles']['fresh']['application_id']};")
    if 'E2_INSTALLED_APP|' + str(inv['roles']['fresh']['application_id']) not in output:
        raise ValueError('Mapped application not installed')
    write_receipt(path / 'qualification.json', {
        'at': now(), 'artifact_sha256': digest(artifact),
        'source_commit': source_binding(path),
        'declaration_sha256': digest(declaration_path(path)),
        'target': inv['roles']['fresh'],
        'state': state, 'checks': 'real fresh target component metadata/greeting/mapped app; GUI evidence separate'})
    print('QUALIFIED observed fresh-target checks; GUI is not claimed by this receipt')


def sentinel(run, role):
    guard(run, role)
    print(sql(run, role, """merge into e2_settings t using (select 'USER_PREFIX' setting_key,'retained-value' setting_value from dual) s
on (t.setting_key=s.setting_key) when not matched then insert(setting_key,setting_value) values(s.setting_key,s.setting_value);
insert into e2_history(greeting_text) select 'E2 retained history' from dual where not exists(select 1 from e2_history where greeting_text='E2 retained history');
commit;"""))
    path, inv = load(run)
    state = target_state(run, role)
    write_json(path / f'preservation-{role}.json', {'at': now(), 'state': state})
    print(state)


def preservation(run, role):
    path, inv = load(run)
    before = json.loads((path / f'preservation-{role}.json').read_text())['state']
    after = target_state(run, role)
    retained = [line for line in before.splitlines()
                if line.startswith('HISTORY|') or line.startswith('SETTING|USER_PREFIX|')]
    if not retained or any(line not in after.splitlines() for line in retained):
        raise ValueError('Retained field-level history/settings changed')
    print('PRESERVED ' + role + ': exact recorded history fields and user setting')


def negative(run, artifact):
    path, inv = guard(run, 'upgrade')
    before = target_state(run, 'upgrade')
    valid = json.loads(declaration_path(path).read_text())
    cases = []
    bad = json.loads(json.dumps(valid)); bad['components']['Foundation'] = '2.0.0'
    cases.append(('incompatible Foundation', bad))
    bad = json.loads(json.dumps(valid)); del bad['dependencies']['Hello']
    cases.append(('missing dependency', bad))
    bad = json.loads(json.dumps(valid)); bad['components']['Hello'] = '9.9.9'
    cases.append(('unknown component version', bad))
    for label, value in cases:
        try:
            validate_contract(value)
        except (ValueError, KeyError):
            print('OBSERVED DECLARATION REJECTION: ' + label)
        else:
            raise ValueError('Unsupported declaration accepted: ' + label)
    receipt = path / 'admission-upgrade.json'
    saved = receipt.read_bytes()
    original_hash = digest(artifact)
    changed = path / 'repo/artifact/e2-negative-input.zip'
    if changed.exists():
        raise ValueError('Retained negative input exists; inspect before retry')
    changed.write_bytes(Path(artifact).read_bytes() + b'\nE2 deliberately changed candidate bytes\n')
    changed_hash = digest(changed)
    try:
        try:
            deploy(run, 'upgrade', changed)
        except ValueError as exc:
            if 'STALE ADMISSION artifact_sha256' not in str(exc):
                raise
            print('OBSERVED CHANGED-ARCHIVE REJECTION BEFORE DEPLOY')
        else:
            raise ValueError('Changed artifact binding was accepted')
    finally:
        changed.unlink()
    held = path / 'admission-upgrade.negative-held'
    if held.exists():
        raise ValueError('An earlier missing-receipt attempt needs inspection')
    receipt.rename(held)
    try:
        try:
            deploy(run, 'upgrade', artifact)
        except FileNotFoundError:
            print('OBSERVED MISSING-RECEIPT REJECTION BEFORE DEPLOY')
        else:
            raise ValueError('Missing receipt was accepted')
    finally:
        held.rename(receipt)
    if receipt.read_bytes() != saved or digest(artifact) != original_hash:
        raise ValueError('Original admission or artifact changed during negative exercise')
    after = target_state(run, 'upgrade')
    if before != after:
        raise ValueError('Target changed during rejected admission')
    write_json(path / 'negative-admission.json', {
        'at': now(), 'before': before, 'after': after,
        'original_artifact_sha256': original_hash, 'changed_input_sha256': changed_hash,
        'cases': ['incompatible Foundation','missing dependency','unknown version','changed archive','missing receipt'],
        'result': 'real target unchanged; native deploy not reached by rejected path',
        'limits': 'declared combinations and bridge control, not native dependency enforcement'})
    print('OBSERVED unchanged real-target state after all rejected inputs')


def titles(run, role, values):
    path, inv = guard(run, role)
    output = sql(run, role, f"set heading off pagesize 0\nselect 'PAGE|'||page_id||'|'||page_title from apex_application_pages where application_id={inv['roles'][role]['application_id']} order by page_id;")
    for value in values.split('|'):
        if value and value not in output:
            raise ValueError('Expected visible page title missing: ' + value)
    print(output)


def identities(run, role, label):
    path, inv = guard(run, role)
    if label not in ('before', 'after'):
        raise ValueError('Use before/after for the bounded replacement-identity observation')
    app_id = inv['roles'][role]['application_id']
    output = sql(run, role, f"""set heading off pagesize 0 linesize 32767
select 'REGION|'||page_id||'|'||region_id||'|'||region_name from apex_application_page_regions where application_id={app_id} order by page_id,region_id;
select 'IR|'||page_id||'|'||report_id||'|'||report_name||'|'||report_type||'|'||application_user||'|'||report_columns from apex_application_page_ir_rpt where application_id={app_id} order by page_id,report_id;
""")
    observed = '\n'.join(x.strip() for x in output.splitlines() if x.strip().startswith(('REGION|','IR|')))
    if not observed:
        raise ValueError('No application region/report identities observed')
    receipt = {'at': now(), 'target': inv['roles'][role], 'observed': observed}
    if label == 'after':
        before = json.loads((path / f'identities-{role}-before.json').read_text())
        receipt['unchanged'] = before['observed'] == observed
        print('REPLACEMENT IDENTITIES UNCHANGED: ' + str(receipt['unchanged']))
    write_receipt(path / f'identities-{role}-{label}.json', receipt)
    print(observed)


def artifact_path(run):
    path, inv = load(run)
    files = sorted((path / 'repo/artifact').rglob('*.zip'), key=lambda x: x.stat().st_mtime)
    if not files:
        raise ValueError('No native artifact exists')
    print(files[-1].resolve())


def patch_resume(run):
    """Admit only the pre-patch boundary; never replay partially applied patch DDL."""
    path, inv = guard(run, 'author')
    repo = path / 'repo'
    if (path / 'B.complete.json').exists():
        raise ValueError('B is complete; use --resume to inspect its completion')
    if git(repo, 'branch', '--show-current') != 'e2-patch':
        raise ValueError('Patch recovery requires the existing e2-patch branch')
    baseline = git(repo, 'rev-parse', 'e2-initial-baseline')
    if git(repo, 'rev-parse', 'HEAD') != baseline or git(repo, 'status', '--porcelain'):
        raise ValueError('Patch recovery requires a clean unchanged initial baseline; patch work may already have started')
    declaration = json.loads(declaration_path(path).read_text())
    if declaration.get('release') != '1.0.0':
        raise ValueError('Patch declaration already advanced; refuse replay')
    columns = sql(run, 'author', "select 'E2_PATCH_COLUMNS|'||count(*) from user_tab_columns where table_name='E2_SETTINGS' and column_name='RELEASE_NOTE';")
    if 'E2_PATCH_COLUMNS|0' not in columns:
        raise ValueError('Patch DDL already started; refuse replay')
    qualified = json.loads((path / 'qualification.json').read_text())
    deployed = json.loads((path / 'deployed-upgrade.json').read_text())
    if qualified['source_commit'] != baseline or qualified['artifact_sha256'] != deployed['artifact_sha256']:
        raise ValueError('Initial qualification/deployment receipts do not match the retained baseline')
    if hashlib.sha256(target_state(run, 'upgrade').encode()).hexdigest() != deployed['state_sha256']:
        raise ValueError('Upgrade target changed since initial delivery; inspect before recovery')
    preservation(run, 'upgrade')
    print('PATCH RESUME READY: initial delivery retained; continuing at Main title/version checkpoint')


def contract_patch(run):
    path, inv = guard(run, 'author')
    file = declaration_path(path)
    value = json.loads(file.read_text())
    value.update(release='1.0.1', stage='complete-patch', supported_starts=['empty', '1.0.0'])
    value['components']['Hello'] = '1.0.1'
    validate_contract(value)
    write_json(file, value)
    print('UPDATED explicit patch declaration; review before commit')


def finish(run, section):
    path, inv = guard(run, 'author')
    head = source_binding(path)
    write_json(path / f'{section}.complete.json', {
        'at': now(), 'section': section, 'source_commit': head,
        'identity': inv['identity'], 'run_id': run})
    print('RECORDED section ' + section + ' completion')


def verify_complete(run, section):
    path, inv = guard(run, 'author')
    receipt = json.loads((path / f'{section}.complete.json').read_text())
    if receipt['identity'] != identity() or receipt['run_id'] != run:
        raise ValueError('Completion belongs to another runtime/run')
    # Later sections legitimately advance HEAD; require the retained checkpoint.
    git(path / 'repo', 'cat-file', '-e', receipt['source_commit'] + '^{commit}')
    source_binding(path)
    print('VERIFIED retained section checkpoint ' + receipt['source_commit'])


def new_fresh(run):
    path, inv = guard(run, 'fresh')
    old = inv['roles']['fresh']
    previous = inv.setdefault('retained_fresh_targets', [])
    allocation = len(previous) + 2
    # Allocate a new owned pair; never erase the earlier qualification target.
    previous.append(old)
    original = previous[0]
    entry = dict(original, schema=original['schema'] + str(allocation), workspace=original['workspace'] + str(allocation),
                 application_id=original['application_id'] + allocation * 1000000,
                 offset=original['offset'] + allocation * 50000)
    user = entry['schema']
    private = json.loads((path / 'private.json').read_text())
    body = f"""declare n number; begin
select count(*) into n from dba_users where username='{user}';
if n>0 then raise_application_error(-20901,'Fresh schema collision'); end if;
select count(*) into n from apex_workspaces where workspace='{entry['workspace']}';
if n>0 then raise_application_error(-20902,'Fresh workspace collision'); end if;
select count(*) into n from apex_applications where application_id={entry['application_id']};
if n>0 then raise_application_error(-20903,'Fresh app collision'); end if;
end;
/
create user {user} identified by "{private['fresh']}" default tablespace USERS quota unlimited on USERS;
grant create session,create table,create view,create procedure,create trigger,create sequence,create type to {user};
create table {user}.e2_run_ownership(run_id varchar2(41) primary key);
insert into {user}.e2_run_ownership values('{run}');
commit;
begin
apex_instance_admin.add_workspace(p_workspace=>'{entry['workspace']}',p_primary_schema=>'{user}');
apex_util.set_workspace(p_workspace=>'{entry['workspace']}');
apex_util.create_user(p_user_name=>'E2DEV',p_web_password=>'{private['developer']}',p_email_address=>'e2@localhost',p_default_schema=>'{user}',p_developer_privs=>'ADMIN:CREATE:DATA_LOADER:EDIT:HELP:MONITOR:SQL',p_change_password_on_first_use=>'N');
commit;
end;
/
"""
    # Persist allocation intent before DDL so partial attempts remain visible.
    write_json(path / 'fresh-allocation.json', {'at': now(), 'target': entry, 'prior': old})
    print(redact(admin_sql(body, admin=True), private))
    inv['roles']['fresh'] = entry
    write_json(path / 'inventory.json', inv)
    guard(run, 'fresh')
    print('ALLOCATED new fresh target; previous target retained')


def stable_capture(run):
    path, inv = guard(run, 'author')
    def inventory():
        return {str(f.relative_to(path / 'repo')): digest(f)
                for f in (path / 'repo/src').rglob('*') if f.is_file()}
    project(run, 'export')
    first = inventory()
    project(run, 'export')
    second = inventory()
    changed = sorted(k for k in set(first) | set(second) if first.get(k) != second.get(k))
    write_json(path / 'capture-stability.json', {'at': now(), 'first': first, 'second': second,
                                               'changed': changed, 'profile': 'native PROJECT original IDs/no export date'})
    print('NO-EDIT CAPTURE changed files: ' + str(len(changed)))
    if changed:
        raise ValueError('No-edit capture differs: ' + ', '.join(changed))


def shared_probe(run, remove=False):
    guard(run, 'author')
    if remove:
        print(sql(run, 'author', 'drop table e2_run_shared_probe purge;'))
    else:
        print(sql(run, 'author', f"create table e2_run_shared_probe as select '{run}' run_id from dual;"))
        print('In Main and Working Copy SQL Workshop select RUN_ID from E2_RUN_SHARED_PROBE; both use the same parsing schema.')


def shared_scope(run, copy_id):
    path, inv = guard(run, 'author')
    copy_id = int(copy_id)
    main_id = inv['roles']['author']['application_id']
    if copy_id == main_id:
        raise ValueError('Working Copy must be distinct from Main')
    schema = inv['roles']['author']['schema']
    output = sql(run, 'author', f"""declare n number; c apex_exec.t_context; value varchar2(100); begin
select count(*) into n from apex_applications where application_id in ({main_id},{copy_id}) and owner='{schema}' and workspace='{schema}';
if n!=2 then raise_application_error(-20910,'Main/copy not in owned author scope'); end if;
for a in (select application_id from apex_applications where application_id in ({main_id},{copy_id}) order by application_id) loop
apex_session.create_session(p_app_id=>a.application_id,p_page_id=>1,p_username=>'E2DEV');
c:=apex_exec.open_query_context(p_location=>apex_exec.c_location_local_db,p_sql_query=>'select run_id from e2_run_shared_probe');
if not apex_exec.next_row(c) then raise_application_error(-20911,'Shared marker missing'); end if;
value:=apex_exec.get_varchar2(c,1);
if value!='{run}' then raise_application_error(-20912,'Foreign shared marker'); end if;
dbms_output.put_line('APP_SHARED_SCHEMA|'||v('APP_ID')||'|{schema}|'||value);
apex_exec.close(c);
apex_session.delete_session;
end loop;
end;
/
""")
    print(output)
    write_receipt(path / 'shared-schema.json', {'at': now(), 'main_id': main_id,
                  'copy_id': copy_id, 'output': output,
                  'method': 'actual public APEX_SESSION/APEX_EXEC contexts; Builder management remains UI-only'})


def lower_compare(run):
    path, inv = guard(run, 'author')
    comparison = path / 'comparison'
    comparison.mkdir(exist_ok=True)
    app_id = inv['roles']['author']['application_id']
    print(sql(run, 'author', f'apex export -applicationid {app_id} -split -skipExportDate -expOriginalIds -expSupportingObjects N', cwd=comparison))
    install = comparison / f'f{app_id}/install.sql'
    if not install.exists():
        raise ValueError('Expected documented split export missing')
    # Evidence-only reconstruction from the same native source checkpoint.
    # Never maintain comparison as a parallel migration authority.
    new_fresh(run)
    path, inv = guard(run, 'fresh')
    target = inv['roles']['fresh']
    source = path / 'repo/src/database' / inv['roles']['author']['schema'].lower()
    files = []
    for group in ('package_specs', 'tables', 'package_bodies'):
        files.extend(sorted((source / group).glob('*.sql')))
    if len(files) != 5:
        raise ValueError('Fixture reconstruction scope changed; inspect complete dependency inventory')
    body = '\n'.join('@"' + str(f.resolve()) + '"' for f in files)
    body += '\n@"' + str(SQL_FIXTURES / 'seed.sql') + '"\n'
    contract = json.loads(declaration_path(path).read_text())
    if contract['components']['Hello'] == '1.0.1':
        body += '@"' + str(SQL_FIXTURES / 'patch.sql') + '"\n'
    body += f"""begin
apex_application_install.set_workspace('{target['workspace']}');
apex_application_install.set_schema('{target['schema']}');
apex_application_install.set_application_id({target['application_id']});
apex_application_install.set_application_alias('E2-LOWER-{target['application_id']}');
apex_application_install.set_offset({target['offset']});
end;
/
@"{install.resolve()}"
"""
    print(sql(run, 'fresh', body))
    state = target_state(run, 'fresh')
    print(state)
    write_json(path / 'lower-reconstruction.json', {'at': now(), 'target': target,
               'source_commit': source_binding(path), 'state': state,
               'split_files': {str(f.relative_to(comparison)): digest(f) for f in comparison.rglob('*.sql')},
               'limits': 'bounded empty-target fixture reconstruction; not E.1 controller or migration-history equivalence'})


def behavior(run, role):
    path, inv = guard(run, role)
    app_id = inv['roles'][role]['application_id']
    output = sql(run, role, f"""declare
q varchar2(32767); c sys_refcursor; d varchar2(4000); r varchar2(4000); n number:=0;
begin
select list_of_values_query into q from apex_application_lovs
where application_id={app_id} and list_of_values_name='E2 GREETING WORDS';
open c for q;
loop fetch c into d,r; exit when c%notfound;
if not ((r='HELLO' and d='Hello') or (r='WORLD' and d='World')) then
raise_application_error(-20920,'Unexpected LOV contract value'); end if;
n:=n+1; dbms_output.put_line('LOV|'||r||'|'||d);
end loop; close c;
if n!=2 then raise_application_error(-20921,'LOV row count differs'); end if;
if e2_greeting.greeting!='Hello World' then raise_application_error(-20922,'Greeting differs'); end if;
dbms_output.put_line('BEHAVIOR|Hello World|LOV return/display contract verified');
end;
/
""")
    print(output)
    write_receipt(path / f'behavior-{role}.json', {'at': now(), 'target': inv['roles'][role],
                  'output': output, 'source_commit': source_binding(path),
                  'limits': 'public metadata query and actual LOV SQL/greeting; browser rendering assessed separately'})


def validate_contract(value):
    spec = importlib.util.spec_from_file_location('e1_compatibility', ROOT / 'scripts/cicd-compatibility.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.validate(value)


def checkpoint(run, section, status, note):
    path, inv = load(run)
    if section not in 'ABCDE' or status not in ('in-progress', 'complete', 'blocked', 'observation'):
        raise ValueError('Invalid checkpoint')
    record = {'at': now(), 'section': section, 'status': status, 'note': note,
              'repo_head': git(path / 'repo', 'rev-parse', 'HEAD')}
    with (path / 'journal.jsonl').open('a') as f:
        f.write(json.dumps(record) + '\n')
    print(json.dumps(record))


def inspect(run, section=None):
    path, inv = load(run)
    print(json.dumps(inv, indent=2))
    file = path / 'journal.jsonl'
    if file.exists():
        for line in file.read_text().splitlines():
            value = json.loads(line)
            if not section or value['section'] == section:
                print(json.dumps(value, indent=2))
    print('EVIDENCE ' + str(path.relative_to(ROOT)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['init','preflight','provision','fixture','app','snapshot','project','deploy','checkpoint','inspect','guard','sql','bind','admit','qualify','sentinel','preservation','negative','titles','identities','artifact-path','contract-patch','patch-resume','finish','verify-complete','new-fresh','stable-capture','shared-probe','shared-scope','lower-compare','behavior'])
    parser.add_argument('--run')
    parser.add_argument('--role', choices=['author','fresh','upgrade'], default='author')
    parser.add_argument('--value')
    parser.add_argument('--file', type=Path)
    parser.add_argument('--section', choices=list('ABCDE'))
    parser.add_argument('--status', default='observation')
    args = parser.parse_args()
    if args.action != 'preflight' and not args.run:
        parser.error('--run required')
    if args.action == 'init': init(args.run)
    elif args.action == 'preflight': preflight(args.run)
    elif args.action == 'provision': provision(args.run)
    elif args.action == 'fixture': fixture(args.run)
    elif args.action == 'app': app(args.run, args.value)
    elif args.action == 'snapshot': print(snapshot(args.run, args.role))
    elif args.action == 'project':
        action, _, value = (args.value or '').partition(':')
        project(args.run, action, value or None)
    elif args.action == 'deploy': deploy(args.run, args.role, args.file)
    elif args.action == 'bind': bind(args.run, args.role, args.file)
    elif args.action == 'admit': admit(args.run, args.role, args.file)
    elif args.action == 'qualify': qualify(args.run, args.file)
    elif args.action == 'sentinel': sentinel(args.run, args.role)
    elif args.action == 'preservation': preservation(args.run, args.role)
    elif args.action == 'negative': negative(args.run, args.file)
    elif args.action == 'titles': titles(args.run, args.role, args.value or '')
    elif args.action == 'identities': identities(args.run, args.role, args.value)
    elif args.action == 'artifact-path': artifact_path(args.run)
    elif args.action == 'contract-patch': contract_patch(args.run)
    elif args.action == 'patch-resume': patch_resume(args.run)
    elif args.action == 'finish': finish(args.run, args.section)
    elif args.action == 'verify-complete': verify_complete(args.run, args.section)
    elif args.action == 'new-fresh': new_fresh(args.run)
    elif args.action == 'stable-capture': stable_capture(args.run)
    elif args.action == 'shared-probe': shared_probe(args.run, args.value == 'remove')
    elif args.action == 'shared-scope': shared_scope(args.run, args.value)
    elif args.action == 'lower-compare': lower_compare(args.run)
    elif args.action == 'behavior': behavior(args.run, args.role)
    elif args.action == 'checkpoint': checkpoint(args.run, args.section, args.status, args.value)
    elif args.action == 'inspect': inspect(args.run, args.section)
    elif args.action == 'guard': guard(args.run, args.role); print('OWNERSHIP VERIFIED ' + args.role)
    elif args.action == 'sql':
        guard(args.run, args.role)
        print(sql(args.run, args.role, '@"' + str(args.file.resolve()) + '"'))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, OSError, RuntimeError, subprocess.SubprocessError) as exc:
        print('BLOCKED: ' + str(exc), file=sys.stderr)
        sys.exit(1)
