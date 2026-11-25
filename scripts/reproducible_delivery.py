"""Bounded ARM64 container delivery experiment; never consumes host credentials."""
import importlib.util, argparse, hashlib, json, math, os, secrets, statistics, subprocess, tempfile, time
from pathlib import Path
VERSION='3.23.0'
SHA='5552106ac866be0c46fdff7a2991a1ed85c0464301a1ac87454c41739d5b6431'
URL=f'https://dl-cdn.alpinelinux.org/alpine/v3.23/releases/aarch64/alpine-minirootfs-{VERSION}-aarch64.tar.gz'
PREFIX=['podman','--connection','apex-cicd']
def validate(path,version,digest=SHA):
 if version!=VERSION:raise ValueError('unqualified tool version')
 if hashlib.sha256(path.read_bytes()).hexdigest()!=digest:raise ValueError('corrupt tool cache')
def summary(values):
 return dict(n=len(values),median=statistics.median(values),p95=sorted(values)[math.ceil(.95*len(values))-1])
def command(args,**kw):
 return subprocess.run(args,check=True,capture_output=True,timeout=90,**kw)
def connection_prefix(connection='apex-cicd'):
 if not connection:raise ValueError('empty connection')
 return ['podman','--connection',connection]
def run(output,connection='apex-cicd'):
 global PREFIX
 PREFIX=connection_prefix(connection)
 root=Path(__file__).resolve().parents[1]
 revision=command(['git','-C',str(root),'rev-parse','HEAD'],text=True).stdout.strip()
 rows=[];markers=[]
 with tempfile.TemporaryDirectory(prefix='e11-delivery-') as td:
  work=Path(td); checkout=work/'source';started=time.monotonic()
  command(['git','clone','--quiet','--no-local',str(root),str(checkout)])
  command(['git','-C',str(checkout),'checkout','--quiet','--detach',revision])
  assert not command(['git','-C',str(checkout),'status','--porcelain'],text=True).stdout.strip()
  checkout_seconds=time.monotonic()-started
  source=checkout/'scripts/isolated_execution.py'
  assert source.is_file()
  # The selected slice executes real hostile candidate commands under E.10's
  # restrictions, using this clean source file as an input whose identity is checked.
  source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
  spec=importlib.util.spec_from_file_location('clean_controller',source)
  controller=importlib.util.module_from_spec(spec);spec.loader.exec_module(controller)
  for sample in range(3):
   cache=work/f'cache-{sample}.tar.gz'
   for mode in ('cold','warm'):
    timings={};started=time.monotonic();fetched=0
    if not cache.exists():
     command(['curl','--fail','--silent','--show-error','--location','--max-time','45',URL,'-o',str(cache)])
     fetched=cache.stat().st_size
    timings['acquire']=time.monotonic()-started
    started=time.monotonic();validate(cache,VERSION);timings['validate']=time.monotonic()-started
    image=None;name='e11-'+secrets.token_hex(10);token=secrets.token_hex(32);markers.append(token)
    try:
     started=time.monotonic()
     image=command(PREFIX+['import','--quiet','--change','LABEL e11.session='+secrets.token_hex(16),str(cache)],text=True).stdout.strip()
     timings['import']=time.monotonic()-started
     script='''set -eu
 test ! -e /run/podman/podman.sock
 test ! -e /var/run/docker.sock
 test -z "${VALIDATOR_TOKEN:-}"
 if touch /forbidden 2>/dev/null; then exit 20; fi
 printf '%s' "$CANDIDATE_CREDENTIAL" > /work/private
 test "$(cat /work/private)" = "$CANDIDATE_CREDENTIAL"
 /bin/busybox | head -1
 echo 'PASS isolated candidate and fresh private input'
 '''
     started=time.monotonic()
     client=controller.Containers(image)
     client.prefix=PREFIX.copy()
     try:name=client.start(script,token)
     except subprocess.CalledProcessError as failure:
      if '--name' in failure.cmd:name=failure.cmd[failure.cmd.index('--name')+1]
      raise RuntimeError(str(failure.stderr).replace(token,'[REDACTED]')) from None
     assert int(client.cli('wait',name).stdout.strip())==0
     result=client.cli('logs',name)
     assert 'BusyBox v1.37.0' in result.stdout,result.stdout
     assert 'PASS isolated candidate and fresh private input' in result.stdout
     timings['execute']=time.monotonic()-started
    finally:
     started=time.monotonic()
     exists=subprocess.run(PREFIX+['container','exists',name],capture_output=True,timeout=10)
     if exists.returncode==0:command(PREFIX+['rm','-f',name])
     assert subprocess.run(PREFIX+['container','exists',name],capture_output=True,timeout=10).returncode==1
     if image:command(PREFIX+['rmi',image])
     timings['cleanup']=time.monotonic()-started
    for marker in markers:assert marker.encode() not in cache.read_bytes()
    rows.append(dict(sample=sample+1,mode=mode,download_bytes=fetched,seconds=timings))
    print(f'PASS sample {sample+1} {mode}: {fetched} downloaded bytes',flush=True)
  bad=work/'bad';bad.write_bytes(b'corrupt')
  for path,version in [(bad,VERSION),(cache,'wrong')]:
   try:validate(path,version)
   except ValueError:pass
   else:raise AssertionError('integrity challenge passed')
  # A truly empty cache succeeded three times; a corrupt cache was rejected,
  # never silently repaired into an apparent cache hit.
  report=dict(checkout_seconds=checkout_seconds,source_revision=revision,source_file='scripts/isolated_execution.py',source_sha256=source_hash,
   tools={'alpine':VERSION,'sha256':SHA,'url':URL,'busybox':'1.37.0',
          'podman':command(PREFIX+['version'],text=True).stdout,
          'python':command(['python3','--version'],text=True).stdout,
          'git':command(['git','--version'],text=True).stdout},samples=rows,
   statistics={mode:{phase:summary([r['seconds'][phase] for r in rows if r['mode']==mode])
    for phase in rows[0]['seconds']} for mode in ('cold','warm')},
   limitations=['Same operator and prepared Podman VM; no independent operator or fresh host claim',
    'Clean source controller executes candidate; workload is the bounded container boundary, not SQLcl/APEX delivery',
    'Cold refers to empty download cache; host/VM storage caches are uncontrolled',
    'Three samples per mode; nearest-rank p95 is the maximum, not a reliable tail estimate'],
   integrity_challenges='wrong release and corrupt bytes rejected before import',credentials='fresh per run; no private files or cache persistence')
  encoded=json.dumps(report,indent=2)+'\n'
  assert all(marker not in encoded for marker in markers)
  output.parent.mkdir(parents=True,exist_ok=True);output.write_text(encoded)
 print('PASS clean checkout, six candidate runs, integrity rejection, scoped cleanup and marker scan')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--connection',default='apex-cicd');args=p.parse_args();run(args.output,args.connection)
