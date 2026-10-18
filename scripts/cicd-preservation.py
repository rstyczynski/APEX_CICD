#!/usr/bin/env python3
"""Field-level retained data comparison. New entries/history may append; old rows cannot change."""
import json,sys
from pathlib import Path
from apex_sql import run
from cicd_environments import canonical

TABLES={'history':('greeting_history','GREETING_ID'),'hello':('hello_entries','ENTRY_ID'),
        'world':('world_entries','ENTRY_ID'),'hello_config':('hello_config','CONFIG_ID'),
        'world_config':('world_config','CONFIG_ID')}

def snapshot(target):
    target = canonical(target)
    if target not in ('user_acceptance_test','integration_test','lab-dev-c'): raise ValueError('Unsupported preservation target')
    body='set heading off feedback off pagesize 0 linesize 32767 sqlformat default\n'
    for label,(table,key) in TABLES.items():
        body+=f"select '{label}|'||json_object(* returning varchar2(4000)) from {table} order by {key};\n"
    output=run(body,connection=target); result={label:{} for label in TABLES}
    for line in output.splitlines():
        label,sep,value=line.strip().partition('|')
        if label in TABLES and sep:
            row=json.loads(value);key=str(row[TABLES[label][1]])
            if key in result[label]: raise ValueError('Duplicate row in preservation snapshot')
            result[label][key]=row
    if len(result['hello_config'])!=1 or len(result['world_config'])!=1:
        raise ValueError('Configuration snapshot missing; refusing an empty/incomplete proof')
    return result

if __name__=='__main__':
    try:
        if len(sys.argv)!=4 or sys.argv[1] not in ('capture','compare'): raise ValueError('Usage: cicd-preservation.py capture|compare TARGET FILE')
        action,target,path=sys.argv[1:]; target=canonical(target); path=Path(path); now=snapshot(target)
        if action=='capture':
            with path.open('x') as f: json.dump({'target':target,'tables':now},f,ensure_ascii=False,indent=2)
            print(f'CAPTURED retained fields: {len(now["history"])} history rows; {path}')
        else:
            saved=json.loads(path.read_text())
            if saved['target']!=target: raise ValueError('Preservation target mismatch')
            for label,rows in saved['tables'].items():
                for key,row in rows.items():
                    if now[label].get(key)!=row: raise ValueError(f'Changed/missing retained row: {label}/{key}')
                if label.endswith('_config') and now[label]!=rows: raise ValueError('Configuration changed')
            print(f'PASS preservation: all fields of {len(saved["tables"]["history"])} prior history rows, old entries and complete configuration unchanged; new rows may append.')
    except (ValueError,OSError,RuntimeError,KeyError) as exc: sys.exit('ERROR: '+str(exc))
