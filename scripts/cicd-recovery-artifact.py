#!/usr/bin/env python3
"""Build/inspect the two bounded BUG-7 experiment artifacts from a pinned Git revision."""
import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import tarfile

ROOT=Path(subprocess.check_output(['git','-C',str(Path(__file__).resolve().parent),'rev-parse','--show-toplevel'],text=True).strip())
FILES=['deploy/recovery/'+n for n in ['control.sql','observe.sql','001-history-index.sql','002-intentional-failure.sql','003-forward-completion.sql','failed.xml','repair.xml']]+['scripts/cicd-recovery-step.py','scripts/cicd-recovery-artifact.py','scripts/apex_sql.py','scripts/cicd_config.py','scripts/cicd_environments.py','scripts/cicd-preservation.py','deploy/operator/fingerprint.sql','deploy/checks/patch_integrity.sql']
sha=lambda data:hashlib.sha256(data).hexdigest()


def inspect(path):
    data=path.read_bytes()
    if sha(data)!=path.with_suffix('.tar.sha256').read_text().strip(): raise ValueError('Recovery archive checksum mismatch')
    files={}
    with tarfile.open(fileobj=io.BytesIO(data)) as t:
        for m in t.getmembers():
            p=PurePosixPath(m.name)
            if not m.isfile() or p.is_absolute() or '..' in p.parts or str(p)!=m.name or m.name in files: raise ValueError('Unsafe recovery archive')
            files[m.name]=t.extractfile(m).read()
    info=json.loads(files.pop('recovery.json'))
    if info['kind'] not in ('failed-additive','forward-repair') or info['target']!='integration_test' or not re.fullmatch('[0-9a-f]{40}',info['source_commit']): raise ValueError('Unsupported recovery artifact')
    if set(files)!=set(FILES) or set(info['files'])!=set(FILES): raise ValueError('Recovery membership differs')
    for name,data in files.items():
        if sha(data)!=info['files'][name]: raise ValueError('Recovery member checksum mismatch')
        # Bind source content to the exact Git revision, not just a self-reported hash list.
        if data!=subprocess.check_output(['git','show',info['source_commit']+':'+name],cwd=ROOT): raise ValueError('Recovery source differs from Git')
    return sha(path.read_bytes()),info,files


def build(revision):
    commit=subprocess.check_output(['git','rev-parse',revision+'^{commit}'],cwd=ROOT,text=True).strip()
    files={n:subprocess.check_output(['git','show',commit+':'+n],cwd=ROOT) for n in FILES}
    for kind in ('failed-additive','forward-repair'):
        info={'format':1,'kind':kind,'target':'integration_test','source_commit':commit,'files':{n:sha(d) for n,d in files.items()}}
        members=dict(files);members['recovery.json']=(json.dumps(info,sort_keys=True,indent=2)+'\n').encode()
        out=io.BytesIO()
        with tarfile.open(fileobj=out,mode='w',format=tarfile.USTAR_FORMAT) as t:
            for name in sorted(members):
                m=tarfile.TarInfo(name);m.size=len(members[name]);m.mode=0o644;m.mtime=0;t.addfile(m,io.BytesIO(members[name]))
        path=ROOT/'.local-apex/releases'/f'{kind}-{commit[:12]}.tar';path.parent.mkdir(parents=True,exist_ok=True)
        with path.open('xb') as f:f.write(out.getvalue())
        path.with_suffix('.tar.sha256').write_text(sha(out.getvalue())+'\n');path.chmod(0o444)
        inspect(path);print('BUILT '+str(path.relative_to(ROOT))+' SHA256 '+sha(out.getvalue()))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['build','inspect']);p.add_argument('value',help='Git revision for build; archive path for inspect');a=p.parse_args()
    try:
        if a.action=='build':build(a.value)
        else:
            digest,info,_=inspect(Path(a.value));print('VERIFIED '+digest+' SOURCE '+info['source_commit']+' KIND '+info['kind'])
    except (ValueError,KeyError,OSError,subprocess.SubprocessError,tarfile.TarError) as exc:p.exit(1,'ERROR: '+str(exc)+'\n')
