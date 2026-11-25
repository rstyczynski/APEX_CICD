"""Build a native release of E6_APP; test schema is never selected."""
from pathlib import Path
import os,subprocess,secrets,re,json,hashlib,zipfile
from contracts_lab import execute as sql,ROOT
from contract_manifest import validate,qualified_toolchain
declarations=json.loads((ROOT/'examples/secure-backend/contracts.json').read_text())
validated_components=validate(declarations)
BUILD=ROOT/'.local-apex/e6/native-project'
BUILD.mkdir(parents=True,exist_ok=True)
EXE=ROOT/'.local-apex/tools/sqlcl-25.4.1.022.0618/sqlcl/bin/sql'
env=os.environ.copy();env['JAVA_HOME']=str(ROOT/'.local-apex/tools/jdk-21.0.12.1+1/Contents/Home')
version=subprocess.check_output([str(EXE),'-version'],env=env,text=True)
qualified_toolchain(json.loads((ROOT/'examples/secure-backend/.dbtools/project.config.json').read_text())['sqlcl']['version'],version)
password=secrets.token_hex(24)
# OS-temporary credentials are never saved in the checkout or native profiles.
setup="alter user E6_APP identified by \""+password+'" account unlock;'
sql(setup,'page-native-auth-start.log',redactions=(password,))
try:
 prefix='whenever sqlerror exit failure rollback\nwhenever oserror exit failure rollback\nconnect E6_APP/"'+password+'"@//127.0.0.1:1521/FREEPDB1\n'
 def run(body,name):
  config=BUILD/'.dbtools/project.config.json'
  if config.exists():assert json.loads(config.read_text())['sqlcl']['version']=='25.4.1.0'
  r=subprocess.run([str(EXE),'-S','-L','/nolog'],input=prefix+body+'\nprompt E6_NATIVE_COMPLETE\nexit\n',cwd=BUILD,env=env,text=True,capture_output=True,timeout=180)
  out=(r.stdout+r.stderr).replace(password,'[REDACTED]')
  (ROOT/'progress/E.6/tests'/name).write_text(out)
  if r.returncode or 'E6_NATIVE_COMPLETE' not in out or re.search(r'(?m)^\s*(ORA-|PLS-|SP2-|ERROR\b|Error starting|Unknown Command)|Expected a subcommand',out):raise RuntimeError(out[-2000:])
  return out
 if not (BUILD/'.dbtools/project.config.json').exists():run('project init -name e6 -schemas E6_APP','native-init.log')
 if not (BUILD/'.git').exists():subprocess.run(['git','init','-b','e6-base'],cwd=BUILD,check=True,capture_output=True)
 def git(*args):return subprocess.check_output(['git',*args],cwd=BUILD,text=True).strip()
 # Establish the empty native project as the compared base exactly once.
 if not subprocess.run(['git','rev-parse','--verify','HEAD'],cwd=BUILD,capture_output=True).returncode==0:
  git('add','.');git('commit','-m','chore: initialize isolated E6 native project')
 if git('branch','--show-current')=='e6-base':git('switch','-c','e6-backend')
 if not (BUILD/'dist/releases/1.0.0/release.changelog.xml').exists():
  run('project export -schemas E6_APP','native-export.log')
  git('add','src');git('commit','-m','feat: capture isolated E6 package-backed application')
  run('project stage -branch-name e6-base\nproject verify -compared-branch-name e6-base -verbose','native-stage-verify.log')
  run('project release -version 1.0.0','native-release.log')
 run('project gen-artifact -name e6-backend -version 1.0.0 -format zip','native-package.log')
 archives=list(BUILD.rglob('*.zip'));assert archives, 'Native artifact missing'
 artifact=max(archives,key=lambda p:p.stat().st_mtime)
 data=artifact.read_bytes();target=ROOT/'progress/E.6/tests'/artifact.name;target.write_bytes(data)
 with zipfile.ZipFile(artifact) as z:
  names=z.namelist();assert names and not any(re.search(r'e6_test|e5_ut|test_contract|e6_test_audit_failure',n,re.I) for n in names)
  assert any('secure_greetings' in n.lower() for n in names), names[:20]
 receipt={'archive':target.name,'sha256':hashlib.sha256(data).hexdigest(),'entries':len(names),'schemas':['E6_APP'],'excluded_test_owners':['E6_TEST','E5_UT'],'sqlcl':version.strip(),'source_commit':git('rev-parse','HEAD'),'component_versions':validated_components,'component_declarations_sha256':hashlib.sha256((ROOT/'examples/secure-backend/contracts.json').read_bytes()).hexdigest()}
 (ROOT/'progress/E.6/tests/native-release.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps(receipt,indent=2))
finally:sql('alter user E6_APP no authentication;','page-native-auth-cleanup.log')
