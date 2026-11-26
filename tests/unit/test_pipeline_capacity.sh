test_pipeline_capacity_arithmetic() {
 python3 - <<'PY'
import sys
from pathlib import Path
import tempfile,json
sys.path.insert(0,'tests')
from pipeline_capacity import distribution,seconds,summarize
assert distribution([10,20])==dict(n=2,median=15,p95=20)
assert seconds('2026-11-26T00:00:02Z')-seconds('2026-11-26T00:00:00Z')==2
for values in [[],[-1],[float('nan')]]:
 try:distribution(values)
 except ValueError:pass
 else:raise AssertionError('invalid samples accepted')
try:summarize(dict(conclusion='failure'),[],Path('.'))
except ValueError:pass
else:raise AssertionError('failed run accepted')
required=['Execute actual utPLSQL regression','Install verified release 1.0.0','Upgrade with verified release 1.1.0','Repeat identical verified release 1.1.0','Verify application after native delivery','Clean job-private connection material','Reject mismatched artifact evidence','Reject mismatched source evidence','Reject actual incompatible SQLcl build','Reject substituted archive bytes']
start='2026-11-26T00:00:00Z';end='2026-11-26T00:00:10Z'
run=dict(id=1,conclusion='success',head_sha='a'*40,created_at=start)
jobs=[]
with tempfile.TemporaryDirectory() as temporary:
 root=Path(temporary)
 for replica in ['1','2']:
  folder=root/('native-1-'+replica);folder.mkdir()
  measurement=dict(GITHUB_SHA='a'*40,GITHUB_RUN_ID='1',CACHE_HIT='true',CACHE_MODE='warm',PARALLEL='2',REPLICA=replica)
  (folder/'measurement.json').write_text(json.dumps(measurement))
  (folder/'success.json').write_text('{"preserved":true}')
  (folder/'utplsql-tests.log').write_text('5 tests, 0 failed, 0 errored')
  (folder/'job.log').write_text('JAVA_HOME: /opt/Java_Temurin-Hotspot_jdk/21.0.13-9/x64')
  (folder/'tool.txt').write_text('SQLcl build 25.4.1.022.0618')
  (folder/'cpu.txt').write_text('Model name: synthetic unit fixture')
  (folder/'memory-start.txt').write_text('Mem: 10000000 0 0 0 0 0')
  (folder/'resources.csv').write_text('unix_seconds,mem_available_kib,cpu_counters,disk_free_bytes\n0,100,1:0:1:5:0:0:0:0,1000\n5,90,2:0:2:6:0:0:0:0,900\n')
  jobs.append(dict(name='native ('+replica+')',conclusion='success',created_at=start,started_at=start,completed_at=end,steps=[dict(name=n,conclusion='success',started_at=start,completed_at=end) for n in required]))
 samples=summarize(run,jobs,root)
 assert len(samples)==2 and samples[0]['execution_seconds']==10 and samples[0]['minimum_disk_free_bytes']==900
 p=root/'native-1-1/measurement.json';m=json.loads(p.read_text());m['CACHE_HIT']='false';p.write_text(json.dumps(m))
 try:summarize(run,jobs,root)
 except ValueError:pass
 else:raise AssertionError('cache miss admitted as warm')
print('PASS synthetic arithmetic and failed-run refusal; no performance claim')
PY
}
