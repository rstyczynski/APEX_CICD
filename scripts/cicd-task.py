#!/usr/bin/env python3
"""Acquire/release component ownership before preparing a task area."""
import argparse
import re
import subprocess
import sys
from apex_sql import run

p = argparse.ArgumentParser()
p.add_argument('action', choices=['acquire', 'release'])
p.add_argument('connection', choices=['lab-dev', 'lab-dev-b', 'lab-dev-c'])
p.add_argument('task')
p.add_argument('scope_or_generation')
args = p.parse_args()
if not re.fullmatch(r'[a-zA-Z0-9_-]{1,80}', args.task):
    p.error('Use a simple task identifier')
try:
    if args.action == 'acquire':
        scope = args.scope_or_generation
        if any(x not in ('Foundation','Hello','World') for x in scope.split(',')):
            p.error('Unknown component scope')
        base = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
        body = f"set serveroutput on\nbegin dbms_output.put_line('Ownership generation: '||E1_CTRL.e1_ownership.acquire('{scope}','{args.task}','{base}')); end;\n/"
    else:
        generation = int(args.scope_or_generation)
        body = f"begin E1_CTRL.e1_ownership.release_task('{args.task}',{generation}); end;\n/"
    print(run(body, connection=args.connection).strip())
except (RuntimeError, ValueError) as exc:
    print(exc, file=sys.stderr)
    sys.exit(1)
