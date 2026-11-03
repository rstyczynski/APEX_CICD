#!/usr/bin/env python3
"""Keep reviewer change labels consistent with the eventual squash message."""
import json
import re
import sys


def classify(pr):
    labels = {x['name'] for x in pr.get('labels', [])}
    if (pr.get('user', {}).get('login') == 'github-actions[bot]'
            and pr.get('head', {}).get('ref', '').startswith('release-please--')
            and 'autorelease: pending' in labels):
        return 'generated-release-pr: review metadata diff and version/changelog'
    selected = labels & {'patch', 'minor', 'major'}
    if len(selected) != 1:
        raise ValueError('Choose exactly one change label: patch, minor, major')
    level = next(iter(selected))
    prefix = {'patch': r'fix(?:\([^\r\n)]+\))?: ',
              'minor': r'feat(?:\([^\r\n)]+\))?: ',
              'major': r'feat(?:\([^\r\n)]+\))?!: '}[level]
    if not re.match(prefix + r'\S[^\r\n]*$', pr.get('title', '')):
        raise ValueError(f'{level} label requires a matching Conventional Commit PR title')
    return level


if __name__ == '__main__':
    try:
        print('PASS PR classification: ' + classify(json.load(open(sys.argv[1]))))
    except (ValueError, KeyError, IndexError) as exc:
        sys.exit(str(exc))
