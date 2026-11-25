"""Trusted bounded laboratory policy. Candidate checkout is never policy authority."""
import hashlib,json
SUITES=('source','migration','compilation','state','backend')
POLICY_HASH=hashlib.sha256(json.dumps({'version':1,'suites':SUITES,'cadences':['pr','scheduled','prerelease']},sort_keys=True).encode()).hexdigest()
def plan(cadence,changed,disabled=()):
 if cadence not in ('pr','scheduled','prerelease'):raise ValueError('Unknown cadence')
 if disabled:raise ValueError('Critical coverage cannot be disabled or quarantined')
 # The bounded greeting journey is one impact unit; every path requires its full inventory.
 return list(SUITES)
def aggregate(required,reports,identity):
 if list(required)!=list(SUITES) or identity.get('policy')!=POLICY_HASH:raise ValueError('Unknown or weakened trusted policy')
 failures=[]
 for suite in required:
  row=reports.get(suite,{})
  if row.get('status')!='success' or type(row.get('count')) is not int or row['count']<=0 or any(row.get(k)!=v for k,v in identity.items()):failures.append(suite)
 return {'success':not failures,'first_failure':failures[0] if failures else None,'failures':failures,'identity':identity,'reports':reports}
