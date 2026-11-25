"""Build a native release of E5_PAGE; test schema is never selected."""
from pathlib import Path
import os,subprocess,secrets,re,json,hashlib,zipfile
from backend_admin import sql,ROOT
BUILD=ROOT/'.local-apex/e5/native-project'
BUILD.mkdir(parents=True,exist_ok=True)
EXE=ROOT/'.local-apex/tools/sqlcl-25.4.1.022.0618/sqlcl/bin/sql'
env=os.environ.copy();env['JAVA_HOME']=str(ROOT/'.local-apex/tools/jdk-21.0.12.1+1/Contents/Home')
version=subprocess.check_output([str(EXE),'-version'],env=env,text=True)
assert '25.4.1.022.0618' in version
password=secrets.token_hex(24)
# OS-temporary credentials are never saved in the checkout or native profiles.
setup="alter user E5_PAGE identified by \""+password+'" account unlock;'
sql(setup,'page-native-auth-start.log')
try:
 prefix='whenever sqlerror exit failure rollback\nwhenever oserror exit failure rollback\nconnect E5_PAGE/"'+password+'"@//127.0.0.1:1521/FREEPDB1\n'
 def run(body,name):
  config=BUILD/'.dbtools/project.config.json'
  if config.exists():assert json.loads(config.read_text())['sqlcl']['version']=='25.4.1.0'
  r=subprocess.run([str(EXE),'-S','-L','/nolog'],input=prefix+body+'\nprompt E5_NATIVE_COMPLETE\nexit\n',cwd=BUILD,env=env,text=True,capture_output=True,timeout=180)
  out=(r.stdout+r.stderr).replace(password,'[REDACTED]')
  (ROOT/'progress/E.5/tests'/name).write_text(out)
  if r.returncode or 'E5_NATIVE_COMPLETE' not in out or re.search(r'(?m)^\s*(ORA-|PLS-|SP2-|ERROR\b|Error starting|Unknown Command)|Expected a subcommand',out):raise RuntimeError(out[-2000:])
  return out
 if not (BUILD/'.dbtools/project.config.json').exists():run('project init -name e5 -schemas E5_PAGE','native-init.log')
 if not (BUILD/'.git').exists():subprocess.run(['git','init','-b','e5-base'],cwd=BUILD,check=True,capture_output=True)
 def git(*args):return subprocess.check_output(['git',*args],cwd=BUILD,text=True).strip()
 # Establish the empty native project as the compared base exactly once.
 if not subprocess.run(['git','rev-parse','--verify','HEAD'],cwd=BUILD,capture_output=True).returncode==0:
  git('add','.');git('commit','-m','chore: initialize isolated E5 native project')
 if git('branch','--show-current')=='e5-base':git('switch','-c','e5-backend')
 if not (BUILD/'dist/releases/1.0.0/release.changelog.xml').exists():
  run('project export -schemas E5_PAGE','native-export.log')
  git('add','src');git('commit','-m','feat: capture isolated E5 package-backed application')
  run('project stage -branch-name e5-base\nproject verify -compared-branch-name e5-base -verbose','native-stage-verify.log')
  run('project release -version 1.0.0','native-release.log')
 run('project gen-artifact -name e5-backend -version 1.0.0 -format zip','native-package.log')
 archives=list(BUILD.rglob('*.zip'));assert archives, 'Native artifact missing'
 artifact=max(archives,key=lambda p:p.stat().st_mtime)
 data=artifact.read_bytes();target=ROOT/'progress/E.5/tests'/artifact.name;target.write_bytes(data)
 with zipfile.ZipFile(artifact) as z:
  names=z.namelist();assert names and not any(re.search(r'e5_test|e5_ut|test_hello_entry|e5_test_ddl',n,re.I) for n in names)
  assert any('hello_entry_api' in n.lower() for n in names), names[:20]
 receipt={'archive':target.name,'sha256':hashlib.sha256(data).hexdigest(),'entries':len(names),'schemas':['E5_PAGE'],'excluded_test_owners':['E5_TEST','E5_UT'],'sqlcl':version.strip(),'source_commit':git('rev-parse','HEAD')}
 (ROOT/'progress/E.5/tests/native-release.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps(receipt,indent=2))
finally:sql('alter user E5_PAGE no authentication;','page-native-auth-cleanup.log')
