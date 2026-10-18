#!/usr/bin/env python3
"""Run/show one visible database isolation operation, or their test sequence."""
import argparse
import json
import re
import sys
from apex_sql import ROOT, run
from cicd_environments import canonical, display

AREAS = json.loads((ROOT/'config/areas.json').read_text())['areas']
FILES = {'identity':'identity.sql', 'create-probe':'create_probe.sql',
         'deny-read':'deny_read.sql', 'deny-write':'deny_write.sql'}


def sql_for(operation, connection, other=None):
    connection = canonical(connection)
    if other is not None: other = canonical(other)
    area = AREAS[connection]
    values = {'schema':area['schema'], 'workspace':area['workspace']}
    if operation.startswith('deny-'):
        if other not in AREAS or other == connection:
            raise ValueError('Choose a different registered area for the access attempt.')
        values['other_schema'] = AREAS[other]['schema']
    sql = (ROOT/'deploy/checks'/FILES[operation]).read_text()
    for key,value in values.items():
        if not re.fullmatch(r'[A-Z][A-Z0-9_]*',value):
            raise ValueError('Unsafe identifier in area configuration')
        sql = sql.replace('{{'+key+'}}',value)
    return sql


def execute(operation, connection, other=None):
    connection = canonical(connection)
    if other is not None: other = canonical(other)
    sql = sql_for(operation,connection,other)
    print(f'OPERATION {operation}: {display(connection)} as {AREAS[connection]["schema"]}',flush=True)
    if operation.startswith('deny-'):
        foreign = AREAS[other]['schema']
        statement = (f'SELECT COUNT(*) FROM {foreign}.E1_PRIVATE_PROBE;' if operation=='deny-read'
                     else f'INSERT INTO {foreign}.E1_PRIVATE_PROBE VALUES (1);')
        print('SQL '+statement,flush=True)
        print('EXPECTED Oracle denies access (ORA-00942 or ORA-01031).',flush=True)
    else:
        print('SQL file: deploy/checks/'+FILES[operation],flush=True)
    result = run(sql,connection=connection)
    for line in result.splitlines():
        if line.startswith('EXPECTED_DENIAL|'):
            _,code,message = line.split('|',2)
            print(f'ACTUAL ORA-{abs(int(code)):05d}: {message}')
        elif line.strip():
            print(line)
    print(f'PASS {operation}: {display(connection)}',flush=True)


def all_checks():
    for name in AREAS:
        execute('create-probe',name)
    names = list(AREAS)
    for index,name in enumerate(names):
        other = names[(index+1)%len(names)]
        execute('deny-read',name,other)
        execute('deny-write',name,other)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('operation',choices=[*FILES,'all','show'])
    p.add_argument('arguments',nargs='*')
    args=p.parse_args()
    try:
        if args.operation=='all':
            all_checks()
        elif args.operation=='show':
            operation,connection,*other=args.arguments
            if operation not in FILES: raise ValueError('Unknown SQL operation')
            print(sql_for(operation,connection,other[0] if other else None),end='')
        else:
            connection,*other=args.arguments
            execute(args.operation,connection,other[0] if other else None)
    except (ValueError,KeyError,RuntimeError) as exc:
        print(exc,file=sys.stderr)
        sys.exit(1)
