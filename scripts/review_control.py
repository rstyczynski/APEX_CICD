"""Bounded Elaboration review policy. Trusted caller must authenticate all inputs.

This library is not a hosted branch protection or authentication service.
"""
import hashlib
import json
ASSESSMENTS=('security','correctness','testing')
def digest(value):
 return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def validate(report,submitter):
 if submitter!='developer': raise ValueError('unauthorized submission')
 if not all(isinstance(report.get(k),str) and report[k] for k in ('base','head','policy')):raise ValueError('missing candidate')
 assessments=report.get('assessments',{})
 if not all(isinstance(assessments.get(k),str) and assessments[k].strip() for k in ASSESSMENTS):raise ValueError('missing assessment')
 if not isinstance(report.get('findings'),list):raise ValueError('missing findings')
 for f in report['findings']:
  if f.get('severity') not in ('info','minor','major','blocker'):raise ValueError('unknown severity')
  if f.get('state') not in ('open','resolved','dismissed'):raise ValueError('unknown disposition')
  if f.get('state') in ('resolved','dismissed') and not (f.get('reason') and f.get('evidence')):raise ValueError('unsupported disposition')
  if f['severity']=='blocker' and f['state']=='open':raise ValueError('unresolved blocker')
 return True
def receipt(report,submitter):
 validate(report,submitter)
 return {'candidate':{k:report[k] for k in ('base','head','policy')},'report':digest(report),'submitter':submitter}
def current(accepted,candidate,report):
 return bool(report and not candidate.get('withdrawn') and accepted['report']==digest(report) and accepted['candidate']=={k:candidate.get(k) for k in ('base','head','policy')})
def publish(accepted,candidate,report,read_current):
 # Read after preparation, immediately before publishing. A hosted adapter still
 # needs serialization/CAS through the actual merge boundary.
 return current(accepted,candidate,report) and current(accepted,read_current(),report)
def authorize(candidate,receipt,report,checks,writer,conversations,approved,bypass=None):
 if bypass and writer=='administrator':return {'allowed':True,'bypass':bypass,'candidate':candidate}
 ok=writer=='integrator' and conversations==0 and approved and current(receipt,candidate,report)
 for name in ('Testing','Review'):
  check=checks.get(name,{})
  ok=ok and check.get('publisher')==name.lower()+'-controller' and check.get('state')=='success' and check.get('candidate')==candidate
 return {'allowed':bool(ok),'bypass':None,'candidate':candidate}
