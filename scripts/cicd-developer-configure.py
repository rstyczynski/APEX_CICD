#!/usr/bin/env python3
"""Configure a single developer's private SQLcl profile without administrator credentials."""
import argparse
import getpass
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from cicd_config import load

ROOT = Path(subprocess.check_output(['git', '-C', str(Path(__file__).resolve().parent), 'rev-parse', '--show-toplevel'], text=True).strip())
MAPPING = {'A': 'lab-dev', 'B': 'lab-dev-b', 'C': 'lab-dev-c'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('developer', choices=MAPPING)
    parser.add_argument('--password-stdin', action='store_true', help='Read only the assigned schema password from stdin; never pass it on the command line')
    args = parser.parse_args()
    config = load(ROOT / 'config/areas.json')
    connection = MAPPING[args.developer]
    area = config['areas'][connection]
    schema = area['schema']
    password = sys.stdin.readline().rstrip('\r\n') if args.password_stdin else getpass.getpass(f'Assigned {schema} schema password: ')
    if not re.fullmatch(r'[A-Za-z0-9_#]+', password):
        raise ValueError('Use the assigned quote-free lab schema password')
    os.umask(0o077)
    profile = ROOT / '.local-apex/developers' / args.developer
    home = profile / 'sqlcl-home'
    home.mkdir(parents=True, mode=0o700, exist_ok=True)
    env = os.environ.copy()
    env['JAVA_HOME'] = str(ROOT / '.local-apex/tools/jdk-21.0.12.1+1/Contents/Home')
    env.pop('JAVA_TOOL_OPTIONS', None)
    # No administrator secret store is opened. Only this password reaches SQLcl.
    body = f'''set echo off verify off define off
whenever oserror exit failure rollback
whenever sqlerror exit failure rollback
connect -save {connection} -savepwd -replace {schema}/"{password}"@//{config['service']}
@"{ROOT}/deploy/operator/identity.sql" {schema} {area['workspace']}
set serveroutput on
begin dbms_output.put_line('DEVELOPER_PROFILE_COMPLETE'); end;
/
exit success
'''
    with tempfile.NamedTemporaryFile(mode='w', suffix='.sql', dir=profile, delete=False) as script:
        script.write(body)
        path = Path(script.name)
    try:
        result = subprocess.run([str(ROOT / '.local-apex/tools/sqlcl/bin/sql'), '-nohistory', '-noupdates', '-home', str(home), '-S', '-L', '/nolog', '@' + str(path)], env=env, cwd=ROOT, capture_output=True, text=True, timeout=120)
    finally:
        path.unlink(missing_ok=True)
    output = (result.stdout + result.stderr).replace(password, '[REDACTED]')
    if result.returncode or not re.search(r'^DEVELOPER_PROFILE_COMPLETE\s*$', output, re.M) or re.search(r'(?m)^\s*(ORA-\d+:|PLS-\d+:|SP2-\d+:|Unknown Command)', output):
        raise RuntimeError(output.strip())
    print(output.strip())
    environment = profile / 'environment.sh'
    environment.write_text('source "$(git rev-parse --show-toplevel)/scripts/cicd-env.sh"\n' + f'export APEX_CICD_CONNECTIONS="$(git rev-parse --show-toplevel)/.local-apex/developers/{args.developer}/sqlcl-home"\n')
    print(f'PASS developer {args.developer}: only {connection} configured in a private profile; no schema/workspace creation.')
    print(f'Next in your terminal: source .local-apex/developers/{args.developer}/environment.sh')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, RuntimeError, OSError, subprocess.SubprocessError) as exc:
        sys.exit('ERROR: ' + str(exc))
