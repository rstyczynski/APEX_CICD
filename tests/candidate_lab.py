"""Real Oracle candidate execution. No retained release report substitutes for execution."""
from pathlib import Path
import sys,subprocess,tempfile,json,re,os,secrets,time
sys.path[:0]=['scripts','tests']
from candidate_testing import plan,aggregate,POLICY_HASH
from contract_manifest import qualified_toolchain
ROOT=Path.cwd();OUT=ROOT/'progress/E.8/tests';OUT.mkdir(exist_ok=True)
BASE=['podman','--connection','apex-cicd','exec','-i','--user','oracle','apex-db','bash','-lc','sqlplus -s / as sysdba']
def sql(body,path):
 r=subprocess.run(BASE,input='whenever sqlerror exit failure rollback\nwhenever oserror exit failure rollback\nset serveroutput on\nset define off\nalter session set container=FREEPDB1;\n'+body+'\nprompt E8_COMPLETE\nexit\n',text=True,capture_output=True,timeout=90)
 text=r.stdout+r.stderr;path.write_text(text)
 if r.returncode or re.search(r'(?m)^\s*(ORA-|PLS-|SP2-|Warning:)',text) or 'E8_COMPLETE' not in text:raise RuntimeError(text[-2000:])
 return text
def git(cwd,*args):return subprocess.check_output(['git','-C',str(cwd),*args],text=True,stderr=subprocess.STDOUT).strip()
def run():
 env=os.environ.copy();env['JAVA_HOME']=str(ROOT/'.local-apex/tools/jdk-21.0.12.1+1/Contents/Home')
 tool=subprocess.check_output([str(ROOT/'.local-apex/tools/sqlcl-25.4.1.022.0618/sqlcl/bin/sql'),'-version'],env=env,text=True)
 qualified_toolchain('25.4.1.0',tool);(OUT/'sqlcl-qualified.log').write_text(tool)
 results=[]
 with tempfile.TemporaryDirectory(prefix='e8-candidate-') as tmp:
  repo=Path(tmp);git(repo,'init','-b','main');git(repo,'config','user.email','lab@example.invalid');git(repo,'config','user.name','E8 laboratory')
  (repo/'migration.sql').write_text("create table @OWNER@.greetings(id number primary key,message varchar2(100));\ninsert into @OWNER@.greetings values(1,'Hello World');\ncommit;\n")
  (repo/'package.sql').write_text("create or replace function @OWNER@.greet return varchar2 is begin return 'Hello World'; end;\n/\n")
  git(repo,'add','.');git(repo,'commit','-m','baseline');ancestor=git(repo,'rev-parse','HEAD');git(repo,'checkout','-b','proposal')
  (repo/'migration.sql').write_text((repo/'migration.sql').read_text()+"alter table @OWNER@.greetings add language_code varchar2(2) default 'en' not null;\n")
  git(repo,'commit','-am','candidate language migration');head=git(repo,'rev-parse','HEAD');git(repo,'checkout','main')
  (repo/'base-marker.txt').write_text('Concurrent accepted base contribution\n');git(repo,'add','.');git(repo,'commit','-m','base advancement');base=git(repo,'rev-parse','HEAD')
  git(repo,'merge','--no-ff','proposal','-m','integrated proposed candidate');merge=git(repo,'rev-parse','HEAD');tree=git(repo,'rev-parse','HEAD^{tree}')
  assert len({ancestor,base,head,merge})==4
  (OUT/'integrated.diff').write_text(git(repo,'diff',base,merge));(OUT/'candidate.bundle').write_bytes(b'')
  git(repo,'bundle','create',str(OUT/'candidate.bundle'),'--all')
  for cadence,fault in [('pr',None),('scheduled',None),('prerelease',None)]+[('pr',f) for f in ['source','migration','compilation','state','backend']]:
   name=cadence+'-'+str(fault);case=OUT/name;case.mkdir(exist_ok=True);owner='E8_'+secrets.token_hex(5).upper();reports={};stages=[];created=False;started=time.monotonic()
   identity={'merge':merge,'tree':tree,'cadence':cadence,'policy':POLICY_HASH}
   required=plan(cadence,['migration.sql','package.sql','base-marker.txt'])
   migration=git(repo,'show',merge+':migration.sql').replace('@OWNER@',owner);package=git(repo,'show',merge+':package.sql').replace('@OWNER@',owner)
   if fault=='migration':migration+='\nalter table '+owner+'.missing_table add broken number;'
   if fault=='compilation':package=package.replace("return 'Hello World'","return missing_identifier")
   if fault=='state':migration=migration.replace('varchar2(2)','varchar2(3)')
   if fault=='backend':package=package.replace('Hello World','Wrong greeting')
   try:
    for suite in required:
     stages.append(suite)
     try:
      if suite=='source':
       if fault=='source':raise ValueError('Injected cheap source rejection')
       assert 'create table' in migration and 'create or replace function' in package
       (case/'source.log').write_text('Integrated merge SQL source accepted; trusted policy selected five mandatory suites\n')
      elif suite=='migration':
       sql('create user '+owner+' no authentication default tablespace users quota 5m on users;',case/'prepare.log');created=True
       sql(migration,case/'migration.log')
      elif suite=='compilation':
       sql(package,case/'compile.log')
       sql("declare n number; begin select count(*) into n from dba_objects where owner='"+owner+"' and status<>'VALID'; if n<>0 then raise_application_error(-20801,'COMPILATION'); end if; end;\n/",case/'compilation.log')
      elif suite=='state':
       sql("declare n number; begin select count(*) into n from dba_tab_columns where owner='"+owner+"' and table_name='GREETINGS' and column_name='LANGUAGE_CODE' and char_length=2 and nullable='N'; if n<>1 then raise_application_error(-20802,'STATE'); end if; end;\n/",case/'state.log')
      elif suite=='backend':
       sql("begin if "+owner+".greet<>'Hello World' then raise_application_error(-20803,'ASSERTION'); end if; dbms_output.put_line('Hello World'); end;\n/",case/'backend.log')
      reports[suite]=dict(identity,status='success',count=1)
     except Exception as e:
      (case/(suite+'-failure.log')).write_text(str(e));reports[suite]=dict(identity,status='failure',count=1);break
   finally:
    if created:sql('drop user '+owner+' cascade;',case/'cleanup.log')
   result=aggregate(required,reports,identity);result.update(base=base,head=head,ancestor=ancestor,stages=stages,fault=fault,elapsed_seconds=round(time.monotonic()-started,3),schema=owner)
   (case/'result.json').write_text(json.dumps(result,indent=2)+'\n');results.append(result)
   assert result['success']==(fault is None),result
   if fault:
    assert result['first_failure']==fault and stages==required[:required.index(fault)+1],result
    diagnostic=(case/(fault+'-failure.log')).read_text()
    expected={'source':'Injected cheap source rejection','migration':'ORA-00942','compilation':'created with compilation errors','state':'STATE','backend':'ASSERTION'}[fault]
    assert expected in diagnostic, 'Unexpected failure cannot satisfy injected case: '+diagnostic
    if fault=='source':assert not (case/'prepare.log').exists()
 (OUT/'executions.json').write_text(json.dumps(results,indent=2)+'\n')
 print('PASS three real integrated candidate cadences and five fail-closed fault paths; scoped cleanup complete')
if __name__=='__main__':run()
