"""Verify a real native run, its immutable workflow and qualified archive bytes."""
import hashlib,json,os,subprocess,tempfile
from pathlib import Path
run=os.environ['E16_RUN_ID'];repo='rstyczynski/APEX_CICD_E.16'
def gh(*args):return subprocess.check_output(['gh',*args],text=True)
r=json.loads(gh('run','view',run,'--repo',repo,'--json','status,conclusion,headSha,jobs'))
assert r['status']=='completed' and r['conclusion']=='success',r
assert all(j['conclusion']=='success' for j in r['jobs'])
with tempfile.TemporaryDirectory(prefix='e16-evidence-') as d:
    gh('run','download',run,'--repo',repo,'--name','native-'+run,'--dir',d)
    root=Path(d)
    assert json.loads((root/'success.json').read_text())['preserved']
    for version in ['1.0.0','1.1.0']:
        receipt=json.loads((root/f'receipt-{version}.json').read_text())
        assert receipt['workflow_source']==r['headSha']
        assert receipt['workflow_run']==run
        assert receipt['build']=='25.4.1.022.0618'
        archive=root/f'native16-{version}.zip'
        assert hashlib.sha256(archive.read_bytes()).hexdigest()==receipt['sha256']
    for case in ['artifact','source','tool','substituted-bytes']:
        assert (root/f'reject-{case}.txt').read_text().strip()
    assert (root/'negative-before.log').read_bytes()==(root/'negative-after.log').read_bytes()
    assert '25.3.0.274.1210' in (root/'incompatible-tool.txt').read_text()
    for name in ['assert-upgrade','assert-repeat']:
        assert 'retained across upgrade' in (root/f'{name}.log').read_text()
print('PASS real native run, provenance bytes, rejection evidence and preserved observations',run,r['headSha'])
