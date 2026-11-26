"""Inspect explicitly selected real native run and its immutable source identity."""
import json,os,subprocess
run=os.environ['E16_RUN_ID'];repo='rstyczynski/APEX_CICD_E.16'
def gh(*args):return subprocess.check_output(['gh',*args],text=True)
r=json.loads(gh('run','view',run,'--repo',repo,'--json','status,conclusion,headSha,jobs'))
assert r['status']=='completed' and r['conclusion']=='success',r
assert all(j['conclusion']=='success' for j in r['jobs'])
print('PASS actual native hosted workflow',run,r['headSha'])
