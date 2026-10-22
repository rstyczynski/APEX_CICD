#!/usr/bin/env python3
"""Display one credential requested by the local operator; never dump the store."""
import argparse
import json
from pathlib import Path
import re
from apex_sql import secrets

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('key', help='For example DEV_A, DEV_B, DEV_C, LAB_USER or APEX_ADMIN_PASSWORD')
p.add_argument('--run', help='E.2 run ID; use with E2DEV to read that run’s Builder password')
args = p.parse_args()
if args.run:
    if args.key != 'E2DEV':
        p.error('--run supports only the E2DEV Builder account')
    if not re.fullmatch(r'[a-z][a-z0-9-]{2,40}', args.run):
        p.error('Invalid E.2 run ID')
    store = Path(__file__).resolve().parent.parent / '.local-apex/e2' / args.run / 'private.json'
    try:
        values = {'E2DEV': json.loads(store.read_text())['developer']}
    except (OSError, ValueError, KeyError):
        p.error('E.2 developer credential unavailable; initialize this run with A --live first')
else:
    values = secrets()
if args.key not in values:
    p.error('Unknown credential key')
print(values[args.key])
