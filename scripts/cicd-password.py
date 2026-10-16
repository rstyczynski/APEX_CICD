#!/usr/bin/env python3
"""Display one credential requested by the local operator; never dump the store."""
import argparse
from apex_sql import secrets

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('key', help='For example DEV_A, DEV_B, DEV_C, LAB_USER or APEX_ADMIN_PASSWORD')
args = p.parse_args()
values = secrets()
if args.key not in values:
    p.error('Unknown credential key')
print(values[args.key])
