"""Snapshot accessible native session records; never reconstruct unavailable turns."""
import datetime,json,os,re
from pathlib import Path
thread=os.environ['CODEX_THREAD_ID']
files=list((Path.home()/'.codex/sessions').rglob('*'+thread+'*.jsonl'))
root=Path(__file__).parent/'chat';root.mkdir(exist_ok=True)
ts=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
base=f'{ts}_{thread}'
records=[]
for f in files:
 for line in f.read_text().splitlines():
  try: records.append(json.loads(line))
  except json.JSONDecodeError: pass
# Redact credential-shaped values without reading unrelated authentication stores.
raw='\n'.join(json.dumps(r,ensure_ascii=False) for r in records)+'\n'
raw=re.sub(r'(?i)(gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|OCID_PRIVATE_KEY[^\\\n]*)','[REDACTED credential]',raw)
(root/(base+'.jsonl')).write_text(raw)
parsed=[json.loads(l) for l in raw.splitlines() if l]
md=['# Accessible native session snapshot','',f'Thread: {thread}. Export: {ts}. Initial execution; no --continue observed.','', 'Coverage: all complete JSONL records accessible at snapshot time. Native writer may lag; records after export are absent. No completeness claim. Credential-shaped values explicitly redacted where matched.','']
for i,r in enumerate(parsed,1):
 md.extend([f'## Record {i}: {r.get("type","unknown")}','', '```json',json.dumps(r,ensure_ascii=False,indent=2),'```',''])
(root/(base+'.md')).write_text('\n'.join(md))
index=root/'index.md'
if not index.exists():index.write_text('# E.19 chat snapshots\n\nNative local session JSONL read interface. Snapshots preserve accessible records chronologically; readable companions retain structured content. No reconstruction. Coverage excludes pending writer buffers, future messages and any inaccessible records.\n\n')
with index.open('a') as f:f.write(f'- [{base}.jsonl]({base}.jsonl), [readable]({base}.md): thread {thread}; exported {ts}; initial execution; records 1–{len(records)} across {len(files)} matching native files; writer lag and later messages excluded.\n')
print(f'Archived {len(records)} records from {len(files)} matching files')
