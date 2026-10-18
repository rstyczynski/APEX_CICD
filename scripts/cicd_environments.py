#!/usr/bin/env python3
"""Public environment names mapped to stable release/connection identities."""
import argparse

ALIASES = {'lab-qualify': 'integration_test', 'lab-test': 'user_acceptance_test'}
IDENTITIES = {'lab-dev', 'lab-dev-b', 'lab-dev-c', 'lab-control', *ALIASES.values()}


def canonical(name):
    value = ALIASES.get(name, name)
    if value not in IDENTITIES:
        raise ValueError('Unknown environment: ' + name)
    return value


def display(name):
    value = canonical(name)
    return canonical(name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('name')
    parser.add_argument('--display', action='store_true')
    args = parser.parse_args()
    try:
        print(display(args.name) if args.display else canonical(args.name))
    except ValueError as exc:
        parser.error(str(exc))
