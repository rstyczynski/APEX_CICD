"""Real technical second operator: isolated nested engine and ephemeral mTLS access."""
import re,hashlib,io,json,os,secrets,subprocess,tarfile,tempfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'progress/E.11/tests/second-operator'
IMAGE='quay.io/podman/stable@sha256:4a53c9400861c466b5c0f8e36eadd93cb644c8234ec4507bc9d40924e34a45ff'
P=['podman','--connection','apex-cicd'];NAME='e11-second-operator-'+secrets.token_hex(5)
def cmd(args,**kw):
 return subprocess.run(args,check=True,capture_output=True,timeout=120,**kw)
def inside(*args,**kw):return cmd(P+['exec','-i',NAME]+list(args),**kw)
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 with tempfile.TemporaryDirectory(prefix='e11-new-access-') as td:
  tmp=Path(td)
  def ssl(*args):cmd(['openssl']+list(args),cwd=tmp)
  ssl('req','-x509','-newkey','rsa:2048','-nodes','-keyout','ca.key','-out','ca.crt','-days','1','-subj','/CN=E11 ephemeral CA')
  for kind in ['server','client']:
   ssl('req','-newkey','rsa:2048','-nodes','-keyout',kind+'.key','-out',kind+'.csr','-subj','/CN=e11-'+kind)
   (tmp/'extensions').write_text('subjectAltName=DNS:localhost,IP:127.0.0.1\nextendedKeyUsage='+('serverAuth' if kind=='server' else 'clientAuth')+'\n')
   ssl('x509','-req','-in',kind+'.csr','-CA','ca.crt','-CAkey','ca.key','-CAcreateserial','-out',kind+'.crt','-days','1','-extfile','extensions')
  cert=cmd(['openssl','x509','-in',str(tmp/'client.crt'),'-noout','-fingerprint','-sha256'],text=True).stdout.strip()
  raw=io.BytesIO()
  with tarfile.open(fileobj=raw,mode='w') as tar:
   for f in ['ca.crt','server.crt','server.key','client.crt','client.key']:tar.add(tmp/f,arcname=f)
  inside('tar','-xf','-','-C','/private',input=raw.getvalue())
  inside('sh','-ec','mkdir -p /home/podman/access; cp /private/ca.crt /private/client.crt /private/client.key /home/podman/access/; chmod 600 /private/*.key /home/podman/access/client.key; chown -R podman:podman /home/podman/access; chmod 700 /home/podman/access')
  inside('sh','-ec',"mkdir -p /etc/containers; printf '[containers]\\nlog_driver=\"k8s-file\"\\ncgroups=\"disabled\"\\n' > /etc/containers/containers.conf")
  # Private CA key never leaves the provisioning temporary directory.
  cmd(P+['exec','-d',NAME,'podman','--storage-driver=vfs','--events-backend=file','--cgroup-manager=cgroupfs','system','service','--time=0','--tls-cert=/private/server.crt','--tls-key=/private/server.key','--tls-client-ca=/private/ca.crt','tcp://127.0.0.1:8443'])
  env=['env','-i','HOME=/home/podman','PATH=/usr/bin:/bin','LANG=C.UTF-8']
  def operator(*args,check=True):
   return subprocess.run(P+['exec','--user','1000:1000',NAME]+env+list(args),check=check,capture_output=True,timeout=120,text=True)
  for attempt in range(20):
   no=operator('curl','--silent','--show-error','--max-time','2','--cacert','/home/podman/access/ca.crt','https://localhost:8443/_ping',check=False)
   if no.returncode and 'certificate' in no.stderr.lower():break
   time.sleep(.25)
  assert no.returncode and 'certificate' in no.stderr.lower(),no.stderr
  (OUT/'denied-without-certificate.log').write_text(no.stderr)
  operator('podman','system','connection','add','second-operator','--tls-ca=/home/podman/access/ca.crt','--tls-cert=/home/podman/access/client.crt','--tls-key=/home/podman/access/client.key','tcp://localhost:8443')
  (OUT/'engine-info.json').write_text(operator('podman','--connection','second-operator','info','--format','json').stdout)
  initial=json.loads(operator('podman','--connection','second-operator','ps','-a','--format','json').stdout)
  images=json.loads(operator('podman','--connection','second-operator','images','--format','json').stdout)
  assert initial==[] and images==[],(initial,images)
  # Export only the two selected public source files, with explicit provenance.
  # No original Git object database, host connections or credentials are copied.
  src=tmp/'slice';src.mkdir();(src/'scripts').mkdir()
  sources={}
  for name in ['isolated_execution.py','reproducible_delivery.py']:
   b=(ROOT/'scripts'/name).read_bytes();(src/'scripts'/name).write_bytes(b);sources[name]=hashlib.sha256(b).hexdigest()
  for args in [['init','-b','main'],['config','user.name','E11 source exporter'],['config','user.email','e11@example.invalid'],['add','scripts'],['commit','-m','Exact E11 selected public source snapshot']]:cmd(['git']+args,cwd=src)
  cmd(['git','bundle','create',str(OUT/'source.bundle'),'HEAD'],cwd=src)
  cmd(P+['cp',str(OUT/'source.bundle'),NAME+':/home/podman/slice.bundle'])
  inside('chown','podman:podman','/home/podman/slice.bundle')
  operator('git','clone','/home/podman/slice.bundle','/home/podman/source')
  assert not operator('git','-C','/home/podman/source','status','--porcelain').stdout.strip()
  print('PASS distinct uid=1000, new mTLS access, unauthenticated rejection, empty independent engine and clean selected-source checkout',flush=True)
  result=operator('python3','/home/podman/source/scripts/reproducible_delivery.py','--connection','second-operator','--output','/home/podman/result.json')
  (OUT/'execution.log').write_text(result.stdout+result.stderr);print(result.stdout,flush=True)
  report=json.loads(operator('cat','/home/podman/result.json').stdout)
  report['limitations'][0]='Technical operator uid 1000, new ephemeral mTLS access and independent nested engine; same physical host/kernel and same orchestrating assistant, no second human claim'
  (OUT/'benchmark.json').write_text(json.dumps(report,indent=2)+'\n')
  assert json.loads(operator('podman','--connection','second-operator','ps','-a','--format','json').stdout)==[]
  assert json.loads(operator('podman','--connection','second-operator','images','--format','json').stdout)==[]
  receipt=dict(operator=operator('id').stdout.strip(),client_certificate_sha256=cert,source_sha256=sources,
   source_base_revision=cmd(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).stdout.strip(),
   selected_source_snapshot=report['source_revision'],image=IMAGE,authentication='fresh ephemeral CA/server/client keys; absent-client TLS handshake rejected',
   isolation='no host mounts or runtime socket; distinct HOME, uid, source repo, engine and image store',
   command='python3 /home/podman/source/scripts/reproducible_delivery.py --connection second-operator --output /home/podman/result.json',
   empty_before=True,empty_after=True,private_access_removed_on_cleanup='outer container and tmpfs must be removed by provisioning controller',
   resource_limit_boundary='Nested runtime cgroups disabled: requested CPU/memory/PID limits are not qualified; candidate shell, credential and filesystem checks unchanged',scope='technical second operator only; no claim of another human, host or full APEX/SQLcl delivery')
  (OUT/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
if __name__=='__main__':
 cmd(P+['run','-d','--name',NAME,'--privileged','--label','e11.experiment=second-operator','--tmpfs','/private:rw,nosuid,mode=700',IMAGE,'sleep','infinity'])
 try:main()
 except subprocess.CalledProcessError as failure:
  OUT.mkdir(parents=True,exist_ok=True)
  (OUT/'failure.log').write_text(re.sub(r'CANDIDATE_CREDENTIAL=[0-9a-f]+','CANDIDATE_CREDENTIAL=[REDACTED]',str(failure)+'\n'+str(failure.stderr)))
  raise
 finally:
  cmd(P+['rm','-f',NAME])
  assert subprocess.run(P+['container','exists',NAME],capture_output=True,timeout=10).returncode==1
  if (OUT/'receipt.json').exists():
   r=json.loads((OUT/'receipt.json').read_text());r['cleanup_verified']=True;(OUT/'receipt.json').write_text(json.dumps(r,indent=2)+'\n')
  print('PASS scoped operator environment and fresh access removed',flush=True)
