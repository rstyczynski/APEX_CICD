"""Bounded release integrity prototype. Trust the supplied manifest digest externally."""
import hashlib,json,zipfile,io
from pathlib import Path

def digest(data): return hashlib.sha256(data).hexdigest()
def build(files,source,release,contracts):
    if not files or not files.get('evidence.txt'): raise ValueError('Missing mandatory evidence')
    manifest={'source':source,'release':release,'contracts':contracts,'files':{k:digest(v) for k,v in files.items()}}
    raw=json.dumps(manifest,sort_keys=True).encode(); stream=io.BytesIO()
    with zipfile.ZipFile(stream,'w') as z:
        z.writestr(zipfile.ZipInfo('manifest.json'),raw)
        for k,v in files.items(): z.writestr(zipfile.ZipInfo(k),v)
    return stream.getvalue(),digest(raw)
def verify(archive,pinned):
    with zipfile.ZipFile(io.BytesIO(archive)) as z:
        names=z.namelist()
        if len(names)!=len(set(names)): raise ValueError('Duplicate members')
        raw=z.read('manifest.json')
        if digest(raw)!=pinned: raise ValueError('Manifest substitution')
        m=json.loads(raw)
        if not m.get('source') or not m.get('contracts') or not m.get('release'): raise ValueError('Missing identity')
        required={'migration.sql','application.sql','configuration.json','contracts.json','evidence.txt'}
        if not required.issubset(m['files']) or set(names)!=set(m['files'])|{'manifest.json'}: raise ValueError('Missing or extra evidence')
        for name,expected in m['files'].items():
            data=z.read(name)
            if not data or digest(data)!=expected: raise ValueError('Artifact or report substitution: '+name)
        return m
