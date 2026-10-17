#!/usr/bin/env python3
"""Small SQLcl boundary: private tools, saved connections and redacted failures."""
from pathlib import Path
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = Path(subprocess.check_output(['git', '-C', str(Path(__file__).resolve().parent), 'rev-parse', '--show-toplevel'], text=True).strip())
LOCAL = ROOT / '.local-apex'


def secrets():
    values = {}
    for line in (LOCAL / 'credentials.env').read_text().splitlines():
        if '=' in line and not line.startswith('#'):
            key, value = line.split('=', 1)
            values[key] = value
    path = LOCAL / 'e1-secrets.json'
    if path.exists():
        values.update(json.loads(path.read_text()))
    return values


def command():
    return [str(LOCAL / 'tools/sqlcl/bin/sql'), '-nohistory', '-noupdates',
            '-home', str(LOCAL / 'tools/sqlcl-home'), '-S', '-L', '/nolog']


def run(body, connection=None, admin=False, save=None):
    private = secrets()
    env = os.environ.copy()
    env['JAVA_HOME'] = str(LOCAL / 'tools/jdk-21.0.12.1+1/Contents/Home')
    env.pop('JAVA_TOOL_OPTIONS', None)
    prefix = 'set echo off verify off feedback off define off\n'
    prefix += 'whenever oserror exit failure rollback\nwhenever sqlerror exit failure rollback\n'
    if admin:
        prefix += 'connect SYS/"' + private['ORACLE_PASSWORD'] + '"@//127.0.0.1:1521/FREEPDB1 as sysdba\n'
    elif save:
        name, user, key = save
        prefix += f'connect -save {name} -savepwd -replace {user}/"{private[key]}"@//127.0.0.1:1521/FREEPDB1\n'
    elif connection:
        if not re.fullmatch(r'[a-z][a-z0-9-]*', connection):
            raise ValueError('Invalid named connection')
        prefix += f'connect -name {connection}\n'
    # A file gives SQLcl its script parser; EOF on piped interactive SQL can
    # otherwise leave statements buffered. Require a server-side end marker.
    script_dir = LOCAL / 'run-sql'
    script_dir.mkdir(mode=0o700, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', dir=script_dir, delete=False) as f:
        f.write('set define off\n' + body + "\nset serveroutput on\nbegin dbms_output.put_line('E1_SQL_COMPLETE'); end;\n/\n")
        script_path = Path(f.name)
    try:
        script = prefix + '@"' + str(script_path) + '"\nexit success\n'
        result = subprocess.run(command(), input=script, text=True, capture_output=True,
                                cwd=ROOT, env=env, timeout=240)
    finally:
        script_path.unlink(missing_ok=True)
    output = result.stdout + result.stderr
    for value in sorted(private.values(), key=len, reverse=True):
        if isinstance(value, str) and value:
            output = output.replace(value, '[REDACTED]')
    if result.returncode or re.search(r'(?m)(ORA-|PLS-|SP2-|Unknown Command|Error starting at line|ERROR:)', output):
        raise RuntimeError(output.strip())
    if not re.search(r'(?m)^E1_SQL_COMPLETE\s*$', output):
        raise RuntimeError('SQLcl did not reach its server-side completion marker.\n' + output.strip())
    return re.sub(r'(?m)^E1_SQL_COMPLETE\s*$', '', output)


if __name__ == '__main__':
    try:
        if sys.argv[1:] == ['--version']:
            env = os.environ.copy()
            env['JAVA_HOME'] = str(LOCAL / 'tools/jdk-21.0.12.1+1/Contents/Home')
            env.pop('JAVA_TOOL_OPTIONS', None)
            subprocess.run(command()[:-1] + ['-version'], env=env, check=True)
        elif len(sys.argv) == 3:
            print(run('@"' + str(Path(sys.argv[2]).resolve()) + '"', connection=sys.argv[1]))
        else:
            raise ValueError('Usage: apex_sql.py --version | CONNECTION SQL_FILE')
    except (ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
