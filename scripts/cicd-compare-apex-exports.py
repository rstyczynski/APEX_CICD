#!/usr/bin/env python3
"""Compare native readable APEX exports; never connect to or modify a database.

The sole comparison exclusion is subscription.version-number in the root app
YAML: APEX increments this revision even after restoring an attribute. This is
an explicit project comparison policy, not native deployment protection.
"""
from pathlib import Path
import re
import sys

REVISION = re.compile(r'(?m)(^subscription:[ \t]*\n  version-number: )[0-9]+(?=\r?$)')


def capture(directory):
    root = Path(directory)
    values = {}
    if not root.is_dir():
        raise ValueError('Missing export directory: '+str(root))
    for p in sorted(root.rglob('*.yaml')):
        content = p.read_text()
        if p.parent.name == 'application' and re.fullmatch(r'f[0-9]+\.yaml', p.name):
            content, count = REVISION.subn(r'\g<1><APEX_REVISION>', content)
            if count != 1:
                raise ValueError('Expected one subscription.version-number in '+str(p))
        values[str(p.relative_to(root))] = content
    if not values:
        raise ValueError('No readable YAML exports in '+str(root))
    return values


def main():
    if len(sys.argv)!=4 or sys.argv[1] not in ('changed','same'):
        raise ValueError('Usage: cicd-compare-apex-exports.py changed|same BEFORE_READABLE AFTER_READABLE')
    left, right = capture(sys.argv[2]), capture(sys.argv[3])
    different = sorted(p for p in left.keys() | right.keys() if left.get(p)!=right.get(p))
    if sys.argv[1]=='changed':
        if not different:
            raise ValueError('Expected a definition change, but exports match')
        print('OBSERVED changed APEX definition files: '+', '.join(different))
    else:
        if different:
            raise ValueError('Unexpected APEX definition differences: '+', '.join(different))
        print('PASS all '+str(len(left))+' exported APEX YAML definitions match')
    print('COMPARISON POLICY: only subscription.version-number is excluded; no database writes')


if __name__=='__main__':
    try:
        main()
    except (ValueError, OSError) as exc:
        print('BLOCKED: '+str(exc),file=sys.stderr)
        sys.exit(1)
