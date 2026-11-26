"""Verify immutable E.18 live-run receipts; no workflow orchestration or simulated outcomes."""
import subprocess,json,sys,tempfile,shutil
from pathlib import Path
sys.path.insert(0,'tests');from clean_host import validate
repo='rstyczynski/APEX_CICD_E.18';runid='45848145737';root=Path('progress/E.18/tests/live-demo');root.mkdir(exist_ok=True)
def data(path):return json.loads(subprocess.check_output(['gh','api',path],text=True))
r=data(f'repos/{repo}/actions/runs/{runid}');jobs=data(f'repos/{repo}/actions/runs/{runid}/jobs?per_page=100')['jobs']
expected=data(f'repos/{repo}/commits/920b1c4')['sha']
if r['conclusion']!='success' or r['head_sha']!=expected:raise RuntimeError('live source/outcome mismatch')
(root/'run.json').write_text(json.dumps(r,indent=2));(root/'jobs.json').write_text(json.dumps(jobs,indent=2))
with tempfile.TemporaryDirectory() as temporary:
 subprocess.run(['gh','run','download',runid,'-R',repo,'-D',temporary],check=True)
 for log in Path(temporary).rglob('utplsql-install.log'):log.write_text(log.read_text().replace('XNtxj8eEgA6X6b6f','[REDACTED vendor default]'))
 shutil.copytree(temporary,root,dirs_exist_ok=True)
for j in jobs:
 if j['conclusion']!='success':raise RuntimeError('live job failed')
 replica=j['name'].split('(')[1].rstrip(')');folder=root/('native-'+runid+'-'+replica)
 validate(folder,runid,r['head_sha'])
 if '5 tests, 0 failed, 0 errored' not in (folder/'utplsql-tests.log').read_text():raise RuntimeError('backend tests missing')
 if not (folder/'application-login-start.png').is_file():raise RuntimeError('blank login capture absent')
 for log in folder.glob('utplsql-install.log'):log.write_text(log.read_text().replace('XNtxj8eEgA6X6b6f','[REDACTED vendor default]'))
 (folder/'job.log').write_text(subprocess.check_output(['gh','api',f"repos/{repo}/actions/jobs/{j['id']}/logs"],text=True).replace('XNtxj8eEgA6X6b6f','[REDACTED vendor default]'))
 print('PASS actual live replica',replica,'source',r['head_sha'],'native archives, preserved row, five backend cases, authenticated access, blank-login capture and private cleanup')
print('PASS live pipeline demonstration; no Product Owner reaction inferred; timing samples remain separate')
