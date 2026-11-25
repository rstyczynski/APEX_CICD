"""Real disposable container experiment; fails on any unmet assertion."""
import concurrent.futures, json, os, secrets, signal, subprocess, sys, tempfile, time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from isolated_execution import Containers, Registry, bounded, review
IMAGE='docker.io/library/alpine@sha256:49340b346798875b5592e5d420241f2f9cfba5f47e62ebb1446a1b34734e898f'
c=Containers(IMAGE); foreign=Containers(IMAGE); outputs=[]
try:
 with tempfile.TemporaryDirectory() as td:
  trusted=Path(td);marker=secrets.token_hex(32)
  (trusted/'validator-policy').write_text(marker)
  payload=f'''test ! -e {trusted}/validator-policy || exit 20
 test ! -e /run/podman/podman.sock || exit 21
 test ! -e /var/run/docker.sock || exit 22
 test -z "$VALIDATOR_TOKEN" || exit 23
 if touch /validator-policy 2>/dev/null; then exit 24; fi
 if mount -t tmpfs tmpfs /mnt 2>/dev/null; then exit 25; fi
 echo "$CANDIDATE_CREDENTIAL" > /work/private
 test "$(cat /work/private)" = "$CANDIDATE_CREDENTIAL" || exit 26
 echo isolated; sleep 120'''
  r=Registry(); identities={}
  with concurrent.futures.ThreadPoolExecutor() as pool:
   futures={s:pool.submit(c.start,payload,'credential-'+s) for s in ('pr-a','pr-b','release')}
   names={s:f.result() for s,f in futures.items()}
  for s,n in names.items():
   identities[s]=r.admit(s,'1','initial')[0]
   assert c.cli('exec',n,'cat','/work/private').stdout.strip()=='credential-'+s
   assert c.cli('exec',n,'sh','-c','test ! -e /work/other').returncode==0
   outputs.append(c.cli('logs',n).stdout)
  assert (trusted/'validator-policy').read_text()==marker
  text='$(touch /work/injected); `id`';assert json.loads(review(text))['review']==text
  assert r.admit('pr-a','1','initial')==(identities['pr-a'],None)
  new,old=r.admit('pr-a','2','supersede');assert old==identities['pr-a'];c.cleanup(names['pr-a'])
  try:r.complete('pr-a',old,'success');raise AssertionError('stale accepted')
  except ValueError:pass
  for s in ('pr-b','release'):
   assert c.cli('inspect',names[s],'--format','{{.State.Running}}').stdout.strip()=='true'
   r.complete(s,identities[s],'success');c.cleanup(names[s])
  r.complete('pr-a',new,'failure');retry,_=r.admit('pr-a','2','deliberate-retry');r.complete('pr-a',retry,'success')
  print('PASS concurrent private data/credentials, own-PR cancellation, independent release, deduplication, stale refusal and deliberate retry')
  for script,expected in [('echo success',0),('echo mandatory-assertion-failure; false',1)]:
   n=c.start(script);assert c.wait(n)==expected
  n=c.start('sleep 120');start=time.monotonic()
  try:c.wait(n,timeout=1);raise AssertionError('hang accepted')
  except subprocess.TimeoutExpired:pass
  assert time.monotonic()-start<35
  print('PASS success/assertion failure/timeout cleanup; assertion failure remains nonzero')
  # A real unavailable runtime endpoint: each subprocess has its own finite deadline.
  attempts=[]
  def unavailable():
   attempts.append(1)
   result=subprocess.run(['podman','--url','tcp://127.0.0.1:1','info'],capture_output=True,timeout=2)
   assert result.returncode!=0
   raise TimeoutError('unavailable runtime')
  try:bounded(unavailable);raise AssertionError('unavailable passed')
  except TimeoutError:pass
  assert len(attempts)==3
  print('PASS unavailable service fails after exactly three bounded transport attempts')
  # A killed controller cannot execute finally: retain and then independently reclaim its orphan.
  other=foreign.start('sleep 120')
  source='''import sys,time\nsys.path.insert(0,'scripts')\nfrom isolated_execution import Containers\nc=Containers(sys.argv[1],sys.argv[2]); print(c.start('sleep 120'),flush=True);time.sleep(120)'''
  child=subprocess.Popen([sys.executable,'-c',source,IMAGE,c.session],stdout=subprocess.PIPE,text=True)
  orphan=child.stdout.readline().strip();assert orphan.startswith('e10-')
  child.kill();child.wait(timeout=5)
  assert c.cli('container','exists',orphan,check=False).returncode==0
  try:foreign.cleanup(orphan);raise AssertionError('foreign cleanup accepted')
  except PermissionError:pass
  assert orphan in c.reap()
  assert foreign.cli('inspect',other,'--format','{{.State.Running}}').stdout.strip()=='true'
  foreign.cleanup(other)
  # Actual cleanup command failure is surfaced; restore trusted transport and retry.
  n=c.start('sleep 120');original=c.prefix;c.prefix=['podman','--url','tcp://127.0.0.1:1']
  try:c.cleanup(n);raise AssertionError('cleanup failure hidden')
  except subprocess.CalledProcessError:pass
  finally:c.prefix=original
  assert n in c.reap()
  assert not c.reap();assert not foreign.reap()
  retained=json.dumps({'output':outputs,'review':review(text),'results':r.results})
  assert marker not in retained and 'credential-pr-' not in retained
  print('PASS privileged access denied, policy preserved, review inert, no markers in retained output/reports/cache (no cache mounted)')
  print('PASS SIGKILL orphan observed/reaped, foreign resources preserved, cleanup failure visible and recovered')
  print('IMAGE '+IMAGE)
finally:
 c.reap();foreign.reap()
