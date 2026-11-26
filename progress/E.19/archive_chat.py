"""Snapshot accessible native session records; never reconstruct unavailable turns."""
import datetime,json,os,re
from pathlib import Path
thread=os.environ['CODEX_THREAD_ID']
context=os.environ.get('E19_ARCHIVE_CONTEXT','continuation after prior incomplete response; same thread')
files=list((Path.home()/'.codex/sessions').rglob('*'+thread+'*.jsonl'))
root=Path(__file__).parent/'chat';root.mkdir(exist_ok=True)
ts=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
base=f'{ts}_{thread}'
records=[]
for f in files:
 for line in f.read_text().splitlines():
  try: records.append(json.loads(line))
  except json.JSONDecodeError: pass
# Native history duplicates tool results in event/world-state records as well.
redacted=0
for record in records:
 encoded=json.dumps(record,ensure_ascii=False)
 if 'facebook.com/' in encoded or 'Documents/Unicredit/' in encoded or 'Facebook, ID:' in encoded:
  payload=record.get('payload',{})
  original_type=payload.get('type') if isinstance(payload,dict) else None
  record['payload']={'redaction':'[REDACTED unrelated personal/work browser content, including duplicate native event/world-state copies; complete payload withheld]', 'original_payload_type':original_type}
  redacted+=1
# Redact credential-shaped values without reading unrelated authentication stores.
raw='\n'.join(json.dumps(r,ensure_ascii=False) for r in records)+'\n'
raw=re.sub(r'(?i)(gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|OCID_PRIVATE_KEY[^\\\n]*)','[REDACTED credential]',raw)
(root/(base+'.jsonl')).write_text(raw)
parsed=[json.loads(l) for l in raw.splitlines() if l]
from chat_markdown import render
markdown,counts=render(parsed,thread,ts,context)
(root/(base+'.md')).write_text(markdown)
conversation,_=render(parsed,thread,ts,context,include_tools=False)
conversation+='\n[Full formatted archive with tool activity](progress/E.19/chat/'+base+'.md)\n'
(Path(__file__).resolve().parents[2]/'chat.md').write_text(conversation)
index=root/'index.md'
if not index.exists():index.write_text('# E.19 chat snapshots\n\nNative local session JSONL read interface. Snapshots preserve accessible records chronologically; readable companions retain structured content. No reconstruction. Coverage excludes pending writer buffers, future messages and any inaccessible records.\n\n')
with index.open('a') as f:f.write(f'- [{base}.jsonl]({base}.jsonl), [readable]({base}.md): thread {thread}; exported {ts}; {context}; records 1–{len(records)} across {len(files)} matching native files; writer lag and later messages excluded.\n')
print(f'Archived {len(records)} records from {len(files)} matching files; readable conversation: {dict(counts)}')
