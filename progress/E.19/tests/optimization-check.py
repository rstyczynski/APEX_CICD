"""Controlled regression: baseline asserts disappear under -O; JS checks remain explicit."""
import subprocess,tempfile,json,hashlib,os
from pathlib import Path
root=Path.cwd()
with tempfile.TemporaryDirectory() as d:
 p=Path(d);archive=p/'archive';archive.write_bytes(b'actual');receipt=p/'receipt';receipt.write_text(json.dumps({'source':'a'*40,'build':'25.4.1.022.0618','sha256':'0'*64}))
 args=[str(root/'sprint-work/E.19/baseline/provenance.py'),str(archive),str(receipt),'a'*40,'25.4.1.022.0618']
 normal=subprocess.run(['python3',*args],capture_output=True,text=True);optimized=subprocess.run(['python3','-O',*args],capture_output=True,text=True)
 env=os.environ.copy();env.update(INPUT_ARCHIVE=str(archive),INPUT_RECEIPT=str(receipt),INPUT_SOURCE='a'*40,INPUT_BUILD='25.4.1.022.0618',GITHUB_OUTPUT=str(p/'output'))
 js=subprocess.run(['node',str(root/'sprint-work/E.19/actions/provenance/index.cjs')],env=env,capture_output=True,text=True)
 if normal.returncode==0 or optimized.returncode!=0 or js.returncode==0:raise RuntimeError('unexpected baseline/replacement behavior')
 print('PASS actual historical baseline rejects mismatch normally but accepts it under Python -O; replacement JavaScript action rejects the same bytes with explicit artifact mismatch. No target operation performed.')
 print(js.stderr.strip())
