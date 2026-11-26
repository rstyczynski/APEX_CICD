"""Audit actual cohort runner namespaces and private cleanup from retained receipts."""
import json
from pathlib import Path
root=Path(__file__).parent/'tests/measurements';data=json.loads((root/'capacity-results.json').read_text());namespaces=set();hosts={};runners=set()
for s in data['samples']:
 run=s['run_id'];replica=s['replica'];folder=root/('native-'+run+'-'+replica)
 host=json.loads((folder/'host.json').read_text());jobs=json.loads((root/('jobs-'+run+'.json')).read_text());job=next(j for j in jobs if j['name']=='native ('+replica+')')
 if host['run']!=run or host['source']!=s['source']:raise ValueError('host receipt binding mismatch')
 if job['runner_id'] in runners:raise ValueError('runner execution identity reused in cohort')
 hosts.setdefault(host['host'],[]).append((run,replica,job['started_at'],job['completed_at']));runners.add(job['runner_id'])
 if len(set(host['database_containers']))!=2:raise ValueError('author and target not distinct')
 for container in host['database_containers']:namespaces.add((job['runner_id'],container))
 if (folder/'cleanup.txt').read_text().strip()!='PASS private inputs removed':raise ValueError('cleanup not observed')
print('PASS',len(data['samples']),'actual successful samples on',len(runners),'distinct ephemeral runner identities;',len(namespaces),'author/target runner namespaces; bound source/run receipts and private cleanup')
for hostname,uses in hosts.items():
 if len(uses)>1:print('OBSERVATION hostname repeats across jobs:',hostname,uses,'; hostname is not treated as physical-host identity')
print('This verifies job namespace separation and recorded cleanup, not physical-host dedication or a cross-tenant penetration test. Fresh input generation remains visible in the executed workflow; private values are not retained.')
