"""Real E.1 regression in an owned PDB; transient private inputs never enter checkout."""
import os,sys,json,secrets,tempfile,subprocess,re,tarfile,io,time,hashlib
from contextlib import ExitStack
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'progress/E.12/tests/legacy-regression'/('run-'+time.strftime('%Y%m%dT%H%M%S')+'-'+str(os.getpid()));OUT.mkdir(parents=True)
REDACTIONS=[]
BASE=['podman','--connection','apex-cicd']
def admin(body):
 sql='whenever sqlerror exit failure rollback\nwhenever oserror exit failure rollback\nset define off\nalter session set container=FREEPDB1;\n'+body+'\nprompt E12_ADMIN_COMPLETE\nexit\n'
 r=subprocess.run(BASE+['exec','-i','--user','oracle','--workdir','/tmp/apex','e12-regression-db','bash','-lc','sqlplus -s / as sysdba'],input=sql,text=True,capture_output=True,timeout=180)
 for value in REDACTIONS:r.stdout=r.stdout.replace(value,'[REDACTED]')
 r.stdout=re.sub(r'(?i)(identified by )"[^"]+"',r'\1"[REDACTED]"',r.stdout)
 if r.returncode or 'E12_ADMIN_COMPLETE' not in r.stdout or re.search(r'(?m)^\s*(ORA-|PLS-|SP2-)',r.stdout):raise RuntimeError(r.stdout[-1500:])
 return r.stdout

def suite(args):
 def source_hashes():
  return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for folder in ['scripts','tests'] for p in (ROOT/folder).rglob('*') if p.is_file() and p.suffix in ('.py','.sh','.sql','.manifest') and '__pycache__' not in p.parts}
 hashes=source_hashes()
 (OUT/'source-snapshot-before.json').write_text(json.dumps(hashes,sort_keys=True,indent=2))
 tool_env=os.environ.copy();tool_env['JAVA_HOME']=str(ROOT/'.local-apex/tools/jdk-21.0.12.1+1/Contents/Home');tool_env.pop('JAVA_TOOL_OPTIONS',None)
 version=subprocess.run([str(ROOT/'.local-apex/tools/sqlcl/bin/sql'),'-version'],env=tool_env,text=True,capture_output=True,timeout=60)
 version_text=version.stdout+version.stderr
 (OUT/'sqlcl-version.log').write_text(version_text)
 if version.returncode or '25.3.0.274.1210' not in version_text:raise RuntimeError('Historical native APEX toolchain mismatch; stopped before target preparation')
 subprocess.run([sys.executable,str(ROOT/'tests/legacy_database.py')],check=True)
 info=json.loads(subprocess.check_output(BASE+['inspect','e12-regression-db'],text=True))[0]
 if info['Config']['Labels'].get('apex.cicd.fixture')!='E12':raise RuntimeError('Unowned regression database container')
 with tempfile.TemporaryDirectory(prefix='e12-regression-private-') as td, ExitStack() as cleanup:
  state=Path(td);state.chmod(0o700);(state/'connections').mkdir()
  (OUT/'patch-selected.txt').write_text((ROOT/'.local-apex/releases/patch-corrected-selected.txt').read_text())
  keys=['ORACLE_PASSWORD','E1_CTRL','E1_DEV_A','E1_DEV_B','E1_DEV_C','E1_INTEGRATION','E1_UAT','LAB_USER','VERIFIER','DEV_A','DEV_B','DEV_C']
  values={k:'Ee12_'+secrets.token_hex(20) for k in keys}
  admin("declare n number; begin select count(*) into n from E12_ADMIN.E12_FIXTURE_OWNER where marker='APEX_CICD_E12_REGRESSION'; if n<>1 then raise_application_error(-20000,'Unowned PDB'); end if; end;\n/")
  values['ORDS_PASSWORD']='Ee12_'+secrets.token_hex(20)
  REDACTIONS.extend(values.values())
  admin(f'''@apex_rest_config_core.sql ./ {values['ORDS_PASSWORD']} {values['ORDS_PASSWORD']}
alter user ANONYMOUS account unlock;
alter user APEX_PUBLIC_USER account unlock;
alter user E12_ADMIN identified by "{values['ORACLE_PASSWORD']}";
grant dba,apex_administrator_role to E12_ADMIN;
begin if sys_context('USERENV','CON_NAME')<>'FREEPDB1' then raise_application_error(-20000,'Wrong regression PDB'); end if; end;
/
declare n number; begin
for r in (select workspace from apex_workspaces where workspace in ('E1_DEV_A','E1_DEV_B','E1_DEV_C','E1_INTEGRATION','E1_UAT')) loop
 apex_instance_admin.remove_workspace(r.workspace,'Y','N');
end loop;
select count(*) into n from dba_users where username='E1_CTRL';
if n=1 then execute immediate 'drop user E1_CTRL cascade'; end if;
end;
/''')
  for name,content in [('credentials.env','ORACLE_PASSWORD='+values['ORACLE_PASSWORD']+'\n'),('e1-secrets.json',json.dumps(values)),('e1-owned.json',(ROOT/'config/areas.json').read_text())]:
   p=state/name;p.write_text(content);p.chmod(0o600)
  os.environ.update(APEX_CICD_STATE=td,APEX_CICD_CONNECTIONS=str(state/'connections'),APEX_CICD_SERVICE='127.0.0.1:1551/FREEPDB1',APEX_CICD_ADMIN_USER='E12_ADMIN',APEX_CICD_ISOLATED_E1='1',APEX_CICD_REGRESSION_EVIDENCE=str(OUT),APEX_CICD_PATCH_SELECTION=str(OUT/'patch-selected.txt'))
  sys.path.insert(0,str(ROOT/'scripts'))
  from apex_sql import run
  def command(*args):
   r=subprocess.run(args,cwd=ROOT,text=True,capture_output=True,timeout=300)
   out=r.stdout+r.stderr
   for value in values.values():out=out.replace(value,'[REDACTED]')
   print(out,flush=True)
   if r.returncode:raise RuntimeError('Regression setup command failed: '+str(args))
  command(sys.executable,'scripts/cicd-platform.py','control-identity')
  print(run('@"'+str(ROOT/'deploy/control.sql')+'"\n@"'+str(ROOT/'deploy/release_control.sql')+'"',connection='lab-control'),flush=True)
  for target in ['lab-dev','lab-dev-b','lab-dev-c','integration_test','user_acceptance_test']:
   command(sys.executable,'scripts/cicd-platform.py','provision',target)
  source=state/'foundation';source.mkdir()
  data=subprocess.check_output(['git','archive','e9a490f0582e768ad822a498453af69aedc9b1e9','apex','db'],cwd=ROOT)
  with tarfile.open(fileobj=io.BytesIO(data)) as tar:tar.extractall(source,filter='data')
  print(run(f'cd "{source}"\nlb update -changelog-file db/changelog.xml\n@"{ROOT}/deploy/operator/import.sql" E1_DEV_A 810001 E1_DEV_A E12-FOUNDATION "{source}/apex/f810001"',connection='lab-dev'),flush=True)
  host_proof=run("set sqlformat csv\nselect sys_context('USERENV','SERVER_HOST') as server_host,sys_context('USERENV','CON_NAME') as pdb from dual;",connection='lab-control')
  assert info['Config']['Hostname'] in host_proof,'Native profile did not reach the owned database container'
  effective=json.loads((ROOT/'config/areas.json').read_text());effective['service']=os.environ['APEX_CICD_SERVICE']
  (OUT/'environment.json').write_text(json.dumps({'container':'e12-regression-db','pdb':'FREEPDB1','service':os.environ['APEX_CICD_SERVICE'],'server_context':host_proof,'sqlcl_build':'25.3.0.274.1210','logical_configuration_sha256':__import__('hashlib').sha256((ROOT/'config/areas.json').read_bytes()).hexdigest(),'effective_configuration_sha256':__import__('hashlib').sha256(json.dumps(effective,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'credential_lifecycle':'fresh OS-private temporary directory, deleted at suite exit','retained_uat_touched':False},indent=2))
  image=re.search(r'^ORDS_IMAGE=(.+)$',(ROOT/'scripts/apex-images.env').read_text(),re.M)[1]
  grants=subprocess.check_output(BASE+['run','--rm','--entrypoint','/bin/cat',image,'/opt/oracle/ords/scripts/installer/ords_installer_privileges.sql'],text=True)
  subprocess.run(BASE+['exec','-i','--user','oracle','e12-regression-db','bash','-lc','cat > /tmp/e12-ords-grants.sql'],input=grants,text=True,check=True)
  admin('@/tmp/e12-ords-grants.sql E12_ADMIN')
  resource='e12-reg-'+secrets.token_hex(6)
  def remove_resources():
   subprocess.run(BASE+['rm','-f',resource],capture_output=True)
   r=subprocess.run(BASE+['volume','rm',resource],capture_output=True,text=True)
   if r.returncode:raise RuntimeError('Private ORDS volume cleanup failed: '+r.stderr)
  command(*BASE,'volume','create',resource)
  cleanup.callback(remove_resources)
  installed=admin("set heading off pagesize 0\nselect 'ORDS_PRESENT='||count(*) from dba_users where username='ORDS_METADATA';")
  if 'ORDS_PRESENT=1' in installed:
   r=subprocess.run(BASE+['run','--rm','-i','--env','JAVA_TOOL_OPTIONS=-Xms64m -Xmx256m','--network','apex-net','-v',resource+':/etc/ords/config:z',image,'uninstall','--admin-user','E12_ADMIN','--db-hostname','e12-regression-db','--db-port','1521','--db-servicename','FREEPDB1','--force','--password-stdin'],input=values['ORACLE_PASSWORD']+'\n',capture_output=True,text=True,timeout=300)
   output=r.stdout+r.stderr
   for value in values.values():output=output.replace(value,'[REDACTED]')
   (OUT/'ords-uninstall.log').write_text(output)
   if r.returncode:raise RuntimeError('Owned isolated ORDS uninstall failed; see redacted log')
  r=subprocess.run(BASE+['run','--rm','-i','--env','JAVA_TOOL_OPTIONS=-Xms64m -Xmx256m','--network','apex-net','-v',resource+':/etc/ords/config:z',image,'install','--admin-user','E12_ADMIN','--proxy-user','--db-hostname','e12-regression-db','--db-port','1521','--db-servicename','FREEPDB1','--gateway-mode','proxied','--gateway-user','APEX_PUBLIC_USER','--password-stdin'],input=values['ORACLE_PASSWORD']+'\n'+values['ORDS_PASSWORD']+'\n',capture_output=True,text=True,timeout=300)
  output=r.stdout+r.stderr
  for value in values.values():output=output.replace(value,'[REDACTED]')
  (OUT/'ords-install.log').write_text(output)
  if r.returncode:raise RuntimeError('Isolated ORDS install failed; see redacted log')
  command(*BASE,'run','--rm','--env','JAVA_TOOL_OPTIONS=-Xms64m -Xmx256m','-v',resource+':/etc/ords/config:z',image,'config','set','standalone.static.path','/opt/oracle/apex/images')
  command(*BASE,'run','-d','--name',resource,'--network','apex-net','-p','127.0.0.1::8080','-v',resource+':/etc/ords/config:z','-v','apex-images:/opt/oracle/apex/images:ro,z','--entrypoint','/opt/graalvm-ee-java17/bin/java',image,'-Xms64m','-Xmx256m','-jar','/opt/oracle/ords/ords.war','--config','/etc/ords/config','serve')
  port=subprocess.check_output(BASE+['port',resource,'8080'],text=True).strip().rsplit(':',1)[1]
  os.environ['APEX_CICD_HTTP_BASE']='http://127.0.0.1:'+port+'/ords/'
  descriptor=json.loads((OUT/'environment.json').read_text());descriptor['http_base']=os.environ['APEX_CICD_HTTP_BASE'];(OUT/'environment.json').write_text(json.dumps(descriptor,indent=2))
  import urllib.request
  for attempt in range(40):
   try:
    urllib.request.urlopen(os.environ['APEX_CICD_HTTP_BASE']+'f?p=810001:9999',timeout=2);break
   except Exception:time.sleep(1)
  else:raise RuntimeError('Isolated ORDS did not become ready')
  manifest=Path(args[args.index('--new-only')+1]) if '--new-only' in args else ROOT/'tests/manifests/component_delivery.manifest'
  selected=manifest.read_text()
  if 'test_IT1_release' not in selected and re.search(r'^integration:test_(release|controls)\.sh:',selected,re.M):
   command(sys.executable,'tests/legacy_release.py','release')
  result=subprocess.run(['bash','tests/run.sh',*args],cwd=ROOT)
  after=source_hashes()
  (OUT/'source-snapshot-after.json').write_text(json.dumps(after,sort_keys=True,indent=2))
  changed=sorted(k for k in hashes.keys()|after.keys() if hashes.get(k)!=after.get(k))
  assert not changed,'Executable source changed during integration; rerun required: '+repr(changed)
  (OUT/'source-snapshot-sha256.json').write_text(json.dumps(hashes,sort_keys=True,indent=2))
  return result.returncode

if __name__=='__main__':
 import fcntl
 # All checkouts share this one real fixture. The kernel releases ownership
 # automatically when the worker exits, including abnormal termination.
 lock_path=Path(tempfile.gettempdir())/'apex-cicd-e12-regression.fixture.lock'
 with lock_path.open('a+') as fixture_lock:
  try:fcntl.flock(fixture_lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
  except BlockingIOError:raise RuntimeError('E.12 regression fixture is owned by another active worker; retry after that worker exits')
  raise SystemExit(suite(sys.argv[1:]))
