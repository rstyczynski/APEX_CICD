#!/usr/bin/env python3
"""Check the retained F archive and prepare local H export directories."""

import hashlib
from pathlib import Path


def prepare(root: Path) -> None:
    lab = root / '.local-apex/e2/project-walkthrough'
    artifact = lab / 'component-repo-f2/artifact/e2-1.0.1-execution-r2.zip'
    expected = artifact.with_suffix('.sha256').read_text().strip()
    if hashlib.sha256(artifact.read_bytes()).hexdigest() != expected:
        raise SystemExit('STOP: F artifact changed')
    evidence = lab / 'h-operator'
    if evidence.exists():
        raise SystemExit('STOP: H evidence already exists; inspect before repeating this chapter')
    evidence.mkdir(mode=0o700)
    for name in ('before', 'drifted', 'after-deploy', 'restored'):
        (evidence / name).mkdir(mode=0o700)
    print('PASS unchanged F artifact; fresh H evidence directories created')


if __name__ == '__main__':
    try:
        prepare(Path(__file__).resolve().parents[1])
    except OSError as error:
        raise SystemExit(f'STOP: {error}') from error
