"""Execute a newly correlated real GitHub-hosted Oracle run, never replay a pass."""
import json, secrets, subprocess, time
repo='rstyczynski/APEX_CICD_E.15'
def gh(*args):
 return subprocess.check_output(['gh',*args],text=True,timeout=40)
correlation='e15-'+secrets.token_hex(12)
print('DISPATCH',correlation,flush=True)
gh('workflow','run','testing.yml','--repo',repo,'-f','correlation='+correlation)
deadline=time.monotonic()+650
while time.monotonic()<deadline:
 runs=json.loads(gh('api',f'repos/{repo}/actions/runs?event=workflow_dispatch&per_page=30'))['workflow_runs']
 matches=[r for r in runs if r['display_title']=='Oracle '+correlation]
 if matches and matches[0]['status']=='completed':
  r=matches[0];print(r['html_url'],r['head_sha'],r['conclusion'],flush=True)
  assert r['conclusion']=='success',r['conclusion']
  jobs=json.loads(gh('api',r['jobs_url']))['jobs']
  oracle=[j for j in jobs if j['name']=='Oracle candidate']
  assert len(oracle)==1 and oracle[0]['conclusion']=='success'
  assert all(j['name'] in ('Oracle candidate','Trusted publisher') for j in jobs)
  assert all(j['conclusion'] in ('success','skipped') for j in jobs)
  log=gh('api',f'repos/{repo}/actions/jobs/{oracle[0]["id"]}/logs')
  assert 'PASS real Oracle greeting' in log and 'HTTP 403' in log and 'Table created.' in log
  print('PASS new hosted Oracle run; real sentinel denial and publication HTTP 403',flush=True)
  break
 time.sleep(10)
else:
 raise TimeoutError('bounded hosted execution deadline')
