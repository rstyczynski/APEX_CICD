"""Capacity receipt arithmetic; successful real workflow evidence is mandatory."""
import csv,datetime,json,math,statistics,subprocess,sys,tempfile,shutil,re
from pathlib import Path

def seconds(s):return datetime.datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()
def distribution(values):
 if not values or any(v<0 or not math.isfinite(v) for v in values):raise ValueError('invalid samples')
 return dict(n=len(values),median=statistics.median(values),p95=sorted(values)[math.ceil(.95*len(values))-1])
def summarize(run,jobs,root):
 if run['conclusion']!='success':raise ValueError('unsuccessful run')
 samples=[]
 for job in jobs:
  if job['conclusion']!='success':raise ValueError('unsuccessful job')
  replica=job['name'].split('(')[1].rstrip(')')
  folder=root/('native-'+str(run['id'])+'-'+replica)
  measurement=json.loads((folder/'measurement.json').read_text())
  if measurement['GITHUB_SHA']!=run['head_sha'] or measurement['GITHUB_RUN_ID']!=str(run['id']):raise ValueError('identity mismatch')
  hit=measurement['CACHE_HIT']=='true'
  if (measurement['CACHE_MODE']=='warm')!=hit:raise ValueError('cache condition not established')
  required=['Execute actual utPLSQL regression','Install verified release 1.0.0','Upgrade with verified release 1.1.0','Repeat identical verified release 1.1.0','Verify application after native delivery','Clean job-private connection material','Reject mismatched artifact evidence','Reject mismatched source evidence','Reject actual incompatible SQLcl build','Reject substituted archive bytes']
  steps={s['name']:s for s in job['steps']}
  if any(steps.get(n,{}).get('conclusion')!='success' for n in required):raise ValueError('mandatory validation missing')
  if '5 tests, 0 failed, 0 errored' not in (folder/'utplsql-tests.log').read_text():raise ValueError('utPLSQL failure')
  if not json.loads((folder/'success.json').read_text())['preserved']:raise ValueError('lost data')
  jdk=sorted(set(re.findall(r'Java_Temurin-Hotspot_jdk/([^/\s]+)/x64',(folder/'job.log').read_text())))
  if not jdk:raise ValueError('actual JDK build missing')
  tool=(folder/'tool.txt').read_text()
  if '25.4.1.022.0618' not in tool:raise ValueError('qualified SQLcl build missing')
  rows=list(csv.DictReader((folder/'resources.csv').open()))
  if len(rows)<2:raise ValueError('missing resource observations')
  first=list(map(int,rows[0]['cpu_counters'].split(':')));last=list(map(int,rows[-1]['cpu_counters'].split(':')))
  delta=[b-a for a,b in zip(first,last)];total=sum(delta[:8]);idle=delta[3]+delta[4]
  memtotal=int(next(l.split()[1] for l in (folder/'memory-start.txt').read_text().splitlines() if l.startswith('Mem:')))
  samples.append(dict(jdk_builds=jdk,sqlcl_build='25.4.1.022.0618',cpu_model=next(l.split(':',1)[1].strip() for l in (folder/'cpu.txt').read_text().splitlines() if l.startswith('Model name:')),replica=replica,cache=measurement['CACHE_MODE'],parallel=int(measurement['PARALLEL']),queue_seconds=seconds(job['started_at'])-seconds(run['created_at']),scheduler_queue_seconds=seconds(job['started_at'])-seconds(job['created_at']),admission_seconds=seconds(job['created_at'])-seconds(run['created_at']),execution_seconds=seconds(job['completed_at'])-seconds(job['started_at']),feedback_seconds=seconds(job['completed_at'])-seconds(run['created_at']),peak_host_used_bytes=memtotal-min(int(r['mem_available_kib'])*1024 for r in rows),minimum_disk_free_bytes=min(int(r['disk_free_bytes']) for r in rows),host_cpu_busy_percent=100*(total-idle)/total,resource_samples=len(rows),phases={n:seconds(s['completed_at'])-seconds(s['started_at']) for n,s in steps.items() if s['conclusion']=='success'}))
 if len(samples)!=2:raise ValueError('expected two independent replicas')
 return samples

def main():
 root=Path(sys.argv[1]);root.mkdir(parents=True,exist_ok=True);runs=sys.argv[2:];samples=[]
 for runid in runs:
  def get(path):return json.loads(subprocess.check_output(['gh','api',path],text=True))
  run=get(f'repos/rstyczynski/APEX_CICD_E.18/actions/runs/{runid}')
  jobs=get(f'repos/rstyczynski/APEX_CICD_E.18/actions/runs/{runid}/jobs?per_page=100')['jobs']
  (root/f'run-{runid}.json').write_text(json.dumps(run,indent=2));(root/f'jobs-{runid}.json').write_text(json.dumps(jobs,indent=2))
  with tempfile.TemporaryDirectory() as temporary:
   subprocess.run(['gh','run','download',runid,'-R','rstyczynski/APEX_CICD_E.18','-D',temporary],check=True)
   for log in Path(temporary).rglob('utplsql-install.log'):
    log.write_text(log.read_text().replace('XNtxj8eEgA6X6b6f','[REDACTED vendor default]'))
   shutil.copytree(temporary,root,dirs_exist_ok=True)
  for job in jobs:
   replica=job['name'].split('(')[1].rstrip(')')
   log=subprocess.check_output(['gh','api',f"repos/rstyczynski/APEX_CICD_E.18/actions/jobs/{job['id']}/logs"],text=True)
   (root/('native-'+runid+'-'+replica)/'job.log').write_text(log.replace('XNtxj8eEgA6X6b6f','[REDACTED vendor default]'))
  samples+=summarize(run,jobs,root)
 groups={}
 for s in samples:groups.setdefault(f"{s['cache']}-parallel-{s['parallel']}",[]).append(s)
 if len(groups)!=4:raise ValueError('missing comparison cell')
 result={k:{metric:distribution([s[metric] for s in v]) for metric in ['queue_seconds','execution_seconds','feedback_seconds','peak_host_used_bytes','minimum_disk_free_bytes','host_cpu_busy_percent']} for k,v in groups.items()}
 (root/'capacity-results.json').write_text(json.dumps(dict(samples=samples,groups=result),indent=2))
 print('PASS four real comparison cells with complete validation; percentiles use nearest rank, n=2 per cell')
if __name__=='__main__':main()
