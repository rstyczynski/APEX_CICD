#!/usr/bin/env python3
"""Bounded Git packaging and safe archive inspection; never connects to Oracle."""
import argparse
import hashlib
import io
import json
import re
from pathlib import Path, PurePosixPath
import subprocess
import tarfile

ROOT = Path(subprocess.check_output(['git', '-C', str(Path(__file__).resolve().parent), 'rev-parse', '--show-toplevel'], text=True).strip())
SCOPE = ['apex', 'db', 'deploy', 'config', 'release', 'tests/sql', 'scripts']

def sha(data):
    return hashlib.sha256(data).hexdigest()

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

def inspect(path):
    data = path.read_bytes()
    digest = sha(data)
    expected = path.with_suffix(path.suffix + '.sha256').read_text().strip()
    if digest != expected:
        raise ValueError('Artifact SHA-256 mismatch')
    with tarfile.open(fileobj=io.BytesIO(data)) as tar:
        files = {}
        for m in tar.getmembers():
            p = PurePosixPath(m.name)
            if not m.isfile() or p.is_absolute() or '..' in p.parts or str(p) != m.name or m.name in files:
                raise ValueError('Unsafe or duplicate archive member')
            files[m.name] = tar.extractfile(m).read()
    info = json.loads(files['artifact.json'])
    if set(files) != set(info['files']) | {'artifact.json'}:
        raise ValueError('Archive membership mismatch')
    for name, expected in info['files'].items():
        if sha(files[name]) != expected:
            raise ValueError('Member checksum mismatch: ' + name)
    if not re.fullmatch(r'[0-9a-f]{40}', info['source_commit']) or not re.fullmatch(r'[0-9a-f]{64}', info['configuration_sha256']):
        raise ValueError('Invalid source/configuration identity')
    if sha(files['config/areas.json']) != info['configuration_sha256']:
        raise ValueError('Configuration digest mismatch')
    candidate = json.loads(files['candidate.json'])
    if candidate['source_commit'] != info['source_commit'] or candidate['status'] != 'passed' or candidate['log_sha256'] != sha(files['candidate.log']):
        raise ValueError('Candidate validation does not match release source')
    manifest = json.loads(files['release/initial.json'])
    if manifest['stage'] != 'complete-initial' or manifest['supported_starts'] != ['empty']:
        raise ValueError('Only the declared empty-target initial release is implemented')
    if manifest['components'] != {'Foundation':'1.0.0','Hello':'1.0.0','World':'1.0.0'}:
        raise ValueError('Unsupported component combination')
    for dependency in ('Hello','World'):
        if manifest['dependencies'][dependency]['Foundation'] != manifest['components']['Foundation']:
            raise ValueError('Incompatible Foundation dependency')
    source = files['apex/f810001/application/create_application.sql'].decode()
    if ",p_flow_status=>'UNAVAILABLE'" not in source:
        raise ValueError('Initial release must import with native UNAVAILABLE status')
    if 'E1_CTRL.e1_release.assert_runtime' not in source:
        raise ValueError('External request gate missing from application initialization')
    for page in (0,1,10,20,100,101,110,111,200,201,210,211,9999):
        if f'apex/f810001/application/pages/page_{page:05}.sql' not in files:
            raise ValueError('Incomplete APEX source')
    return digest, info, files

def build():
    if git('status','--porcelain','--untracked-files=all','--',*SCOPE).strip():
        raise ValueError('Dirty release source set; review and commit before build')
    commit = git('rev-parse','HEAD').decode().strip()
    files = {}
    for raw in git('ls-tree','-rz','--name-only',commit,'--',*SCOPE).split(b'\0'):
        if raw:
            name = raw.decode()
            files[name] = git('show',commit+':'+name)
    candidate_dir = ROOT/'.local-apex/releases/candidates'
    candidate = (candidate_dir/(commit+'.json')).read_bytes()
    candidate_log = (candidate_dir/(commit+'.log')).read_bytes()
    receipt = json.loads(candidate)
    if receipt['source_commit'] != commit or receipt['status'] != 'passed' or receipt['log_sha256'] != sha(candidate_log):
        raise ValueError('Missing/mismatched candidate validation')
    files['candidate.json'] = candidate
    files['candidate.log'] = candidate_log
    info = {'format':1,'source_commit':commit,'files':{n:sha(v) for n,v in files.items()},
            'configuration_sha256':sha(files['config/areas.json'])}
    files['artifact.json'] = (json.dumps(info,sort_keys=True,indent=2)+'\n').encode()
    out = ROOT/'.local-apex/releases'/('lab-1.0.0-'+commit[:12]+'.tar')
    out.parent.mkdir(parents=True,exist_ok=True)
    if out.exists() or out.with_suffix('.tar.sha256').exists():
        raise ValueError('Retained artifact already exists; never overwrite')
    archive = io.BytesIO()
    with tarfile.open(fileobj=archive,mode='w',format=tarfile.USTAR_FORMAT) as tar:
        for name in sorted(files):
            value = files[name]
            member = tarfile.TarInfo(name)
            member.size, member.mode, member.mtime = len(value), 0o644, 0
            tar.addfile(member,io.BytesIO(value))
    payload = archive.getvalue()
    with out.open('xb') as f:
        f.write(payload)
    with out.with_suffix('.tar.sha256').open('x') as f:
        f.write(sha(payload)+'\n')
    out.chmod(0o444)
    out.with_suffix('.tar.sha256').chmod(0o444)
    inspect(out)
    (out.parent/'initial-selected.txt').write_text(str(out.relative_to(ROOT))+'\n')
    print('BUILT '+str(out.relative_to(ROOT)))
    print('SHA256 '+sha(payload))
    print('SOURCE '+commit)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['build','inspect','unpack'])
    p.add_argument('archive',nargs='?',type=Path)
    p.add_argument('destination',nargs='?',type=Path)
    a=p.parse_args()
    try:
        if a.action=='build':
            if a.archive or a.destination: p.error('build takes no paths')
            build()
        else:
            if not a.archive: p.error('archive path required')
            digest,info,files=inspect(a.archive)
            if a.action=='unpack':
                if not a.destination or a.destination.exists():
                    raise ValueError('A fresh unpack destination is required')
                a.destination.mkdir(parents=True,mode=0o700)
                for name,value in files.items():
                    dest=a.destination/name
                    dest.parent.mkdir(parents=True,exist_ok=True)
                    dest.write_bytes(value)
            print('VERIFIED SHA256 '+digest)
            print('SOURCE '+info['source_commit'])
            print('CONFIGURATION '+info['configuration_sha256'])
    except (ValueError,KeyError,OSError,tarfile.TarError,subprocess.CalledProcessError) as exc:
        p.exit(1,'ERROR: '+str(exc)+'\n')

if __name__ == "__main__":
    main()
