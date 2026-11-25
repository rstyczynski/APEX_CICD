#!/usr/bin/env python3
"""Small SQLcl boundary: private tools, saved connections and redacted failures."""
from pathlib import Path
import json
import os
import re
import subprocess
import sys
import tempfile
from contextlib import nullcontext
from cicd_environments import canonical
from cicd_config import load, validate

ROOT = Path(subprocess.check_output(['git', '-C', str(Path(__file__).resolve().parent), 'rev-parse', '--show-toplevel'], text=True).strip())
TOOLS = ROOT / '.local-apex'
LOCAL = Path(os.environ.get('APEX_CICD_STATE', str(TOOLS)))


def secrets():
    values = {}
    if LOCAL.resolve() != TOOLS.resolve():
        if LOCAL.resolve().is_relative_to(ROOT.resolve()):
            raise ValueError('Private state must be outside the checkout')
        for line in (LOCAL / 'credentials.env').read_text().splitlines():
            if '=' in line and not line.startswith('#'):
                key, value = line.split('=', 1)
                values[key] = value
    path = LOCAL / 'e1-secrets.json'
    if path.exists():
        values.update(json.loads(path.read_text()))
    return values


def command():
    return [str(TOOLS / 'tools/sqlcl/bin/sql'), '-nohistory', '-noupdates',
            '-home', os.environ.get('APEX_CICD_CONNECTIONS', str(Path.home())), '-S', '-L', '/nolog']


def run(body, connection=None, admin=False, save=None):
    if connection is not None:
        connection = canonical(connection)
    config = load(ROOT / 'config/areas.json')
    config['service'] = os.environ.get('APEX_CICD_SERVICE', config['service'])
    validate(config)
    profile = os.environ.get('APEX_CICD_CONNECTIONS')
    if profile and Path(profile).resolve().is_relative_to(ROOT.resolve()):
        raise ValueError('Native connection profiles must be outside the checkout')
    if LOCAL.resolve() == TOOLS.resolve() and (admin or save):
        raise ValueError('Administrative/provisioning calls require explicit private inputs outside the checkout')
    direct_author = connection in ('lab-dev','lab-dev-b','lab-dev-c') and not profile
    private = secrets() if LOCAL.resolve() != TOOLS.resolve() or direct_author else {}
    env = os.environ.copy()
    env['JAVA_HOME'] = str(TOOLS / 'tools/jdk-21.0.12.1+1/Contents/Home')
    env.pop('JAVA_TOOL_OPTIONS', None)
    prefix = 'set echo off verify off feedback off define off\n'
    prefix += 'whenever oserror exit failure rollback\nwhenever sqlerror exit failure rollback\n'
    if admin:
        admin_user = os.environ.get('APEX_CICD_ADMIN_USER', 'SYS')
        if not re.fullmatch(r'[A-Z][A-Z0-9_]*', admin_user):
            raise ValueError('Invalid admin identity')
        prefix += 'connect ' + admin_user + '/"' + private['ORACLE_PASSWORD'] + '"@//' + config['service'] + (' as sysdba' if admin_user == 'SYS' else '') + '\n'
    elif save:
        name, user, key = save
        prefix += f'connect -save {name} -savepwd -replace {user}/"{private[key]}"@//{config["service"]}\n'
    elif connection:
        if not re.fullmatch(r'[a-z][a-z0-9_-]*', connection):
            raise ValueError('Invalid named connection')
        if profile:
            prefix += f'connect -name {connection}\n'
        else:
            if connection not in ('lab-dev','lab-dev-b','lab-dev-c'):
                raise ValueError('This role requires an explicit native profile outside the checkout')
            user = config['areas'][connection]['schema']
            prefix += f'connect {user}/"{private[user]}"@//{config["service"]}\n'
    # A file gives SQLcl its script parser; EOF on piped interactive SQL can
    # otherwise leave statements buffered. Require a server-side end marker.
    script_dir = LOCAL / 'run-sql'
    script_dir.mkdir(mode=0o700, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', dir=script_dir, delete=False) as f:
        f.write('set define off\n' + body + "\nset serveroutput on\nbegin dbms_output.put_line('E1_SQL_COMPLETE'); end;\n/\n")
        script_path = Path(f.name)
    try:
        script = prefix + '@"' + str(script_path) + '"\nexit success\n'
        with (tempfile.TemporaryDirectory(prefix='apex-sql-native-') if not profile else nullcontext(None)) as native_home:
            args = command()
            if native_home:
                args[args.index('-home')+1] = native_home
            result = subprocess.run(args, input=script, text=True, capture_output=True,
                                    cwd=ROOT, env=env, timeout=240)
    finally:
        script_path.unlink(missing_ok=True)
    output = result.stdout + result.stderr
    for value in sorted(private.values(), key=len, reverse=True):
        if isinstance(value, str) and value:
            output = output.replace(value, '[REDACTED]')
    if result.returncode or re.search(r'(?m)^\s*(?:ORA-[0-9]{5}:|PLS-[0-9]{5}:|SP2-[0-9]+:|Unknown Command|Error starting at line|ERROR(?: at line|:))', output):
        raise RuntimeError(output.strip())
    if not re.search(r'(?m)^E1_SQL_COMPLETE\s*$', output):
        raise RuntimeError('SQLcl did not reach its server-side completion marker.\n' + output.strip())
    return re.sub(r'(?m)^E1_SQL_COMPLETE\s*$', '', output)


if __name__ == '__main__':
    try:
        if sys.argv[1:] == ['--version']:
            env = os.environ.copy()
            env['JAVA_HOME'] = str(TOOLS / 'tools/jdk-21.0.12.1+1/Contents/Home')
            env.pop('JAVA_TOOL_OPTIONS', None)
            subprocess.run(command()[:-1] + ['-version'], env=env, check=True)
        elif len(sys.argv) == 3:
            print(run('@"' + str(Path(sys.argv[2]).resolve()) + '"', connection=sys.argv[1]))
        else:
            raise ValueError('Usage: apex_sql.py --version | CONNECTION SQL_FILE')
    except (ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
