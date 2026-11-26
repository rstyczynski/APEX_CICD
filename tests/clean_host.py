"""Read E.17 actual hosted observations; never simulate the platform."""
import hashlib,json,os,subprocess,tempfile
from pathlib import Path

def validate(root,run,source):
 host=json.loads((root/'host.json').read_text())
 assert host['run']==run and host['source']==source
 assert host['host'] and host['identity'] and len(set(host['database_containers']))==2
 assert 'new random per-run' in host['fresh_inputs']
 access=json.loads((root/'application-access.json').read_text())
 assert access['status']==200 and access['login']
 assert 'APEX Delivery Laboratory' in (root/'application.html').read_text()
 assert (root/'cleanup.txt').read_text().strip()=='PASS private inputs removed'
 assert json.loads((root/'success.json').read_text())['preserved']
 for v in ['1.0.0','1.1.0']:
  r=json.loads((root/f'receipt-{v}.json').read_text())
  assert r['workflow_source']==source and r['workflow_run']==run
  assert r['build']=='25.4.1.022.0618'
  assert hashlib.sha256((root/f'native16-{v}.zip').read_bytes()).hexdigest()==r['sha256']
 for label in ['assert-upgrade','assert-repeat']:
  assert 'retained across upgrade' in (root/f'{label}.log').read_text()

def verify_review():
 repo='rstyczynski/APEX_CICD_E.17';candidate=repo+'-candidates'
 def data(*args):return json.loads(subprocess.check_output(['gh',*args],text=True))
 good=data('run','view','45819877026','-R',repo,'--json','conclusion,jobs')
 assert good['conclusion']=='success'
 steps={s['name']:s['conclusion'] for j in good['jobs'] for s in j['steps']}
 for name in ['Challenge publication authority','Verify trusted Review matches candidate bytes','Execute bounded application-user SQL']:assert steps[name]=='success'
 stale=data('run','view','45820491077','-R',repo,'--json','conclusion,jobs')
 steps={s['name']:s['conclusion'] for j in stale['jobs'] for s in j['steps']}
 assert stale['conclusion']=='failure' and steps['Verify trusted Review matches candidate bytes']=='failure'
 assert steps['Execute bounded application-user SQL']=='skipped'
 pr=data('api',f'repos/{candidate}/pulls/1')
 assert pr['merged'] and pr['head']['sha']=='556adf7f63d9b8b0d334bd6c782df543de304c6c'
 protection=data('api',f'repos/{candidate}/branches/main/protection')
 assert protection['enforce_admins']['enabled'] and 'TrustedOracle' in protection['required_status_checks']['contexts']
 assert not data('api',f'repos/{candidate}/actions/permissions')['enabled']
 print('PASS fresh E17 Review and Oracle, stale rejection before execution, protected ordinary merge and candidate execution boundary')

def main():
 run=os.environ['E17_RUN_ID'];repo='rstyczynski/APEX_CICD_E.17'
 def gh(*args):return subprocess.check_output(['gh',*args],text=True)
 r=json.loads(gh('run','view',run,'-R',repo,'--json','status,conclusion,headSha,jobs'))
 assert r['status']=='completed' and r['conclusion']=='success'
 steps={s['name']:s['conclusion'] for j in r['jobs'] for s in j['steps']}
 for name in ['Install verified release 1.0.0','Upgrade with verified release 1.1.0','Repeat identical verified release 1.1.0','Verify application after native delivery','Clean job-private connection material']:
  assert steps.get(name)=='success',name
 with tempfile.TemporaryDirectory() as d:
  gh('run','download',run,'-R',repo,'-n','native-'+run,'-D',d)
  validate(Path(d),run,r['headSha'])
  for line in (Path(d)/'reviewed-inputs.sha256').read_text().splitlines():
   digest,name=line.split(maxsplit=1)
   raw=subprocess.check_output(['gh','api',f"repos/{repo}/contents/{name}?ref={r['headSha']}",'-H','Accept: application/vnd.github.raw+json'])
   assert hashlib.sha256(raw).hexdigest()==digest,name
 verify_review()
 print('PASS actual independent hosted platform, application access, native delivery and cleanup',run)
if __name__=='__main__':main()
