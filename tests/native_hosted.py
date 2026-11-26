"""Verify a real native run, its immutable workflow and qualified archive bytes."""
import hashlib,json,os,subprocess,tempfile
from pathlib import Path
run=os.environ['E16_RUN_ID'];repo='rstyczynski/APEX_CICD_E.16'
def gh(*args):return subprocess.check_output(['gh',*args],text=True)
r=json.loads(gh('run','view',run,'--repo',repo,'--json','status,conclusion,headSha,jobs'))
assert r['status']=='completed' and r['conclusion']=='success',r
assert all(j['conclusion']=='success' for j in r['jobs'])
required=['Export source 1.0.0','Stage changes 1.0.0','Verify changes 1.0.0','Prepare release 1.0.0','Package release 1.0.0','Install verified release 1.0.0','Export source 1.1.0','Stage changes 1.1.0','Verify changes 1.1.0','Prepare release 1.1.0','Package release 1.1.0','Upgrade with verified release 1.1.0','Repeat identical verified release 1.1.0','Assert retained data after upgrade','Assert retained data after repeat','Reject mismatched artifact evidence','Reject mismatched source evidence','Reject actual incompatible SQLcl build','Reject substituted archive bytes','Assert refusal cases preserved target','Clean job-private connection material']
steps={s['name']:s['conclusion'] for j in r['jobs'] for s in j['steps']}
assert all(steps.get(name)=='success' for name in required),steps
with tempfile.TemporaryDirectory(prefix='e16-evidence-') as d:
    gh('run','download',run,'--repo',repo,'--name','native-'+run,'--dir',d)
    root=Path(d)
    assert json.loads((root/'success.json').read_text())['preserved']
    for version in ['1.0.0','1.1.0']:
        receipt=json.loads((root/f'receipt-{version}.json').read_text())
        assert receipt['workflow_source']==r['headSha']
        assert receipt['workflow_run']==run
        assert receipt['reviewed_inputs_sha256']==hashlib.sha256((root/'reviewed-inputs.sha256').read_bytes()).hexdigest()
        assert receipt['build']=='25.4.1.022.0618'
        archive=root/f'native16-{version}.zip'
        assert hashlib.sha256(archive.read_bytes()).hexdigest()==receipt['sha256']
    for case in ['artifact','source','tool','substituted-bytes']:
        assert (root/f'reject-{case}.txt').read_text().strip()
    assert (root/'negative-before.log').read_bytes()==(root/'negative-after.log').read_bytes()
    assert '25.3.0.274.1210' in (root/'incompatible-tool.txt').read_text()
    for name in ['assert-upgrade','assert-repeat']:
        assert 'retained across upgrade' in (root/f'{name}.log').read_text()
print('PASS named Actions lifecycle, real native run, provenance bytes, rejection evidence and preserved observations',run,r['headSha'])
