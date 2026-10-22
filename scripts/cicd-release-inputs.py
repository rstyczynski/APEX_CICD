#!/usr/bin/env python3
"""Reconstruct exact reviewed release inputs from Git and pinned original evidence."""
import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import tarfile

ROOT = Path(subprocess.check_output(['git', '-C', str(Path(__file__).resolve().parent), 'rev-parse', '--show-toplevel'], text=True).strip())


def sha(value):
    return hashlib.sha256(value).hexdigest()


def payload(recipe, root=ROOT):
    if recipe['format'] != 1 or not re.fullmatch(r'[0-9a-f]{64}', recipe['archive_sha256']):
        raise ValueError('Invalid release input recipe')
    descriptor = recipe['artifact_json'].encode()
    info = json.loads(descriptor)
    commit = info['source_commit']
    if not re.fullmatch(r'[0-9a-f]{40}', commit):
        raise ValueError('Full pinned source revision required')
    subprocess.run(['git', 'cat-file', '-e', commit+'^{commit}'], cwd=root, check=True, capture_output=True)
    files = {}
    for name, digest in info['files'].items():
        p = PurePosixPath(name)
        if p.is_absolute() or '..' in p.parts or str(p) != name:
            raise ValueError('Unsafe recipe path')
        if name in ('candidate.json', 'candidate.log'):
            value = recipe['evidence'][name].encode()
        else:
            if p.parts[0] not in ('apex', 'db', 'deploy', 'config', 'release', 'scripts', 'tests'):
                raise ValueError('Unexpected source scope')
            value = subprocess.check_output(['git', 'show', commit+':'+name], cwd=root)
        if sha(value) != digest:
            raise ValueError('Source/evidence digest mismatch: '+name)
        files[name] = value
    files['artifact.json'] = descriptor
    result = io.BytesIO()
    with tarfile.open(fileobj=result, mode='w', format=tarfile.USTAR_FORMAT) as archive:
        for name in sorted(files):
            member = tarfile.TarInfo(name)
            member.size, member.mode, member.mtime = len(files[name]), 0o644, 0
            archive.addfile(member, io.BytesIO(files[name]))
    data = result.getvalue()
    if sha(data) != recipe['archive_sha256']:
        raise ValueError('Reconstructed archive hash differs from reviewed release')
    return commit, data


def prepare(root=ROOT):
    # Validate/reconstruct both completely before writing either active pointer.
    prepared = []
    for name in ('initial', 'patch'):
        recipe = json.loads((root/'release/inputs'/f'{name}.json').read_text())
        commit, data = payload(recipe, root)
        version = '1.0.0' if name == 'initial' else '1.0.1'
        path = root/'.local-apex/releases'/f'lab-{version}-{commit[:12]}.tar'
        checksum = path.with_suffix('.tar.sha256')
        for existing, expected in ((path, data), (checksum, (sha(data)+'\n').encode())):
            if existing.exists() and existing.read_bytes() != expected:
                raise ValueError('Conflicting retained input; inspect without overwriting: '+str(existing.relative_to(root)))
        prepared.append((name, path, checksum, data))
    for name, path, checksum, data in prepared:
        path.parent.mkdir(parents=True, exist_ok=True)
        for dest, value in ((path, data), (checksum, (sha(data)+'\n').encode())):
            if not dest.exists():
                with dest.open('xb') as f:
                    f.write(value)
                dest.chmod(0o444)
        pointer = path.parent/(name+'-selected.txt')
        temporary = pointer.with_suffix('.tmp')
        temporary.write_text(str(path.relative_to(root))+'\n')
        temporary.replace(pointer)
        print(f'RECONSTRUCTED {name}: {path.relative_to(root)} SHA256 {sha(data)}')
    print('PASS release inputs: exact reviewed bytes reconstructed; no Oracle connection or new candidate-test claim.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    try:
        prepare()
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as exc:
        parser.exit(1, 'ERROR: '+str(exc)+'\nA complete Git history with the pinned source commits is required; no release input is downloaded implicitly.\n')
