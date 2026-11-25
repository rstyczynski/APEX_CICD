"""Fixed isolated E.6 Oracle boundary; no stored database passwords."""
from pathlib import Path
from contextlib import contextmanager
import subprocess,secrets,re,json,sys,os,time
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'progress/E.6/tests'
SQL=ROOT/'examples/secure-backend/sql'
BASE=['podman','--connection','apex-cicd','exec','-i','--user','oracle','apex-db','bash','-lc','sqlplus -s / as sysdba']
PREFIX='''whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
set define off
set sqlblanklines on
set pagesize 0
set linesize 32767
set long 10000000
set longchunksize 32767
set feedback off
set heading off
set verify off
alter session set container=FREEPDB1;
'''
def command(body,user=None,password=None):
 prefix=PREFIX
 if user:
  assert user in ('E6_APP','E6_TEST')
  prefix+='connect '+user+'/"'+password+'"@//localhost:1521/FREEPDB1\n'
 return prefix+'set serveroutput on\n'+body+'\nprompt E6_COMPLETE\nexit\n'
def execute(body,name,user=None,password=None,allow_error=False,redactions=()):
 r=subprocess.run(BASE,input=command(body,user,password),text=True,capture_output=True,timeout=90)
 output=r.stdout+r.stderr
 for value in ((password,) if password else ())+tuple(redactions):
  output=output.replace(value,'[REDACTED]')
 OUT.mkdir(parents=True,exist_ok=True);(OUT/name).write_text(output)
 bad=r.returncode or re.search(r'(?m)^\s*(ORA-|PLS-|SP2-|Warning:)',output) or 'E6_COMPLETE' not in output
 if bad and not allow_error:raise RuntimeError(output[-2500:])
 return output
@contextmanager
def access(user):
 assert user in ('E6_APP','E6_TEST')
 password=secrets.token_hex(24)
 execute('alter user '+user+' identified by "'+password+'" account unlock;','auth-start-'+user+'.log',allow_error=False,redactions=(password,))
 try:yield password
 finally:execute('alter user '+user+' no authentication;','auth-cleanup-'+user+'.log')
def unit(expected_failure=False,name='unit.log'):
 with access('E6_TEST') as pw:
  out=execute("select * from table(e5_ut.ut.run('e6_test.test_contract'));",name,'E6_TEST',pw)
 if expected_failure:assert re.search(r'3 tests, [12] failed, 0 errored',out),out
 else:assert '3 tests, 0 failed, 0 errored, 0 disabled' in out,out
 print('PASS '+('incompatible result detected' if expected_failure else '3 real utPLSQL consumers'))
def init_session(country='PL',identity='ALICE'):
 assert country in ('PL','DE') and identity in ('ALICE','BOB')
 return "begin apex_session.create_session(p_app_id=>810603,p_page_id=>1,p_username=>'"+identity+"'); apex_util.set_session_state('P1_COUNTRY','"+country+"'); end;\n/\n"
def end_session():return "begin apex_session.delete_session(apex_application.g_instance); end;\n/\n"
def compatibility():
 current=(SQL/'greeting_contract.sql').read_text()
 # The pre-extension 1.0 contract has no suffix or structured renderer.
 baseline=current.replace(', p_suffix varchar2 default null','').replace('||p_suffix','')
 baseline=re.sub(r' function render_v2\(p_text varchar2\) return varchar2;\n','',baseline)
 baseline=re.sub(r' function render_v2\(p_text varchar2\) return varchar2 is.*?\n end;\n', '',baseline,flags=re.S)
 baseline=baseline.replace("return 'Hello '||trim(p_text);","return 'Hello '||p_text;")
 patch=baseline.replace("return 'Hello '||p_text;","return 'Hello '||trim(p_text);")
 try:
  execute('alter session set current_schema=E6_APP;\n'+baseline,'compat-baseline-install.log');unit(name='compat-1.0.log')
  execute('alter session set current_schema=E6_APP;\n'+patch,'compat-patch-install.log');unit(name='compat-1.0.1.log')
  with access('E6_TEST') as pw:
   fixed=execute("select e6_app.greeting_contract.render('  World  ') from dual;",'compatible-patch-fix.log','E6_TEST',pw)
   assert 'Hello World' in fixed and 'Hello   World' not in fixed,fixed
  execute('alter session set current_schema=E6_APP;\n'+current,'compat-minor-install.log');unit(name='compat-1.1.log')
  with access('E6_TEST') as pw:
   out=execute("select e6_app.greeting_contract.render('World','!') from dual;\nselect e6_app.greeting_contract.render_v2('World') from dual;",'compatible-additions.log','E6_TEST',pw)
   assert 'Hello World!' in out and '"message":"Hello World"' in out,out
  mutant=current.replace("return 'Hello '||trim(p_text)||p_suffix;","return 'BREAKING RESULT';")
  execute('alter session set current_schema=E6_APP;\n'+mutant,'incompatible-install.log');unit(True,'incompatible-detected.log')
 finally:execute('alter session set current_schema=E6_APP;\n'+current,'compat-restored.log')
 unit(name='compat-restored-consumers.log')
 print('PASS baseline/patch/minor consumers, additions, detected break and restoration')

def sessions_transactions():
 import selectors
 fixture=ROOT/'tests/sql/contracts'
 session_before=execute("select 'SESSION_COUNT:'||count(*) from apex_workspace_sessions where workspace_name='E6_APP';",'sessions-before.log')
 before=execute("select country_code||':'||request_key||':'||greeting_text||':'||actor from e6_app.greeting_requests order by 1;",'business-before.log')
 with access('E6_TEST') as pw:
  execute((fixture/'session_transactions.sql').read_text(),'sessions.log','E6_TEST',pw)
  execute((fixture/'fault_setup.sql').read_text(),'fault-setup.log')
  try:
   execute((fixture/'partial_failure.sql').read_text(),'partial-failure.log','E6_TEST',pw)
   out=execute("select 'PARTIAL_ROWS:'||count(*) from e6_app.greeting_requests where request_key='FAIL-AUDIT';\nselect 'MARKERS:'||count(*) from e6_test.caller_markers;",'partial-invariants.log')
   assert 'PARTIAL_ROWS:0' in out and 'MARKERS:0' in out,out
  finally:execute('drop trigger e6_app.e6_test_audit_failure;','fault-cleanup.log')
  def race(first_action):
   key='E6-'+first_action+'-'+secrets.token_hex(6)
   prefix=init_session()+"begin dbms_application_info.set_module('E6_RACE_A',null); secure_greetings.submit_request('"+key+"','PL','World'); dbms_output.put_line('E6_LOCK_HELD'); end;\n/\n"
   # E6_TEST has execute grants but no direct access to business tables.
   prefix=prefix.replace(' secure_greetings.',' e6_app.secure_greetings.')
   a=subprocess.Popen(BASE,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
   a.stdin.write((command(prefix,'E6_TEST',pw).split('prompt E6_COMPLETE')[0]).encode());a.stdin.flush()
   seen=b'';selector=selectors.DefaultSelector();selector.register(a.stdout,selectors.EVENT_READ)
   deadline=time.monotonic()+15
   while b'E6_LOCK_HELD' not in seen:
    assert time.monotonic()<deadline,'First writer did not acquire the row'
    if selector.select(.2):seen+=os.read(a.stdout.fileno(),65536)
    assert a.poll() is None,seen.decode()
   expect=-20403 if first_action=='commit' else 0
   second=init_session()+"begin dbms_application_info.set_module('E6_RACE_B',null); end;\n/\n"+f"""declare l_code number:=0;
begin
 begin e6_app.secure_greetings.submit_request('{key}','PL','World');
 exception when others then l_code:=sqlcode; end;
 if l_code<>{expect} then raise_application_error(-20484,'Wrong competing result: '||l_code); end if;
 commit;
 dbms_output.put_line('E6_SECOND_EXPECTED:{expect}');
end;
/
"""+end_session()
   b=subprocess.Popen(BASE,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
   b.stdin.write(command(second,'E6_TEST',pw).encode());b.stdin.close();b.stdin=None
   try:
    blocked=False
    for _ in range(30):
     out=execute("select 'TX_WAIT:'||count(*) from v$session where module='E6_RACE_B' and event='enq: TX - row lock contention' and state='WAITING';",'race-'+first_action+'-wait.log')
     if 'TX_WAIT:1' in out:blocked=True;break
     assert b.poll() is None,'Second writer finished before its interleaving'
     time.sleep(.1)
    assert blocked,'No observed Oracle unique-key transaction wait'
    a.stdin.write((first_action+';\n'+end_session()+'prompt E6_FIRST_COMPLETE\nexit\n').encode());a.stdin.close();a.stdin=None
    more=a.communicate(timeout=15)[0];first=(seen+more).decode();second_out=b.communicate(timeout=15)[0].decode()
    (OUT/('race-'+first_action+'-first.log')).write_text(first.replace(pw,'[REDACTED]'))
    (OUT/('race-'+first_action+'-second.log')).write_text(second_out.replace(pw,'[REDACTED]'))
    assert a.returncode==b.returncode==0 and 'E6_FIRST_COMPLETE' in first and 'E6_COMPLETE' in second_out,(first,second_out)
    assert not re.search(r'(?m)^\s*(ORA-|PLS-|SP2-)',first+second_out),(first,second_out)
    check=execute("select 'REQUESTS:'||count(*) from e6_app.greeting_requests where request_key='"+key+"';\nselect 'AUDITS:'||count(*) from e6_app.greeting_audit where request_key='"+key+"';",'race-'+first_action+'-invariants.log')
    assert 'REQUESTS:1' in check and 'AUDITS:1' in check,check
   finally:
    for proc in (a,b):
     if proc.poll() is None:proc.kill();proc.wait(timeout=10)
    execute("delete from e6_app.greeting_audit where request_key='"+key+"';\ndelete from e6_app.greeting_requests where request_key='"+key+"';\ncommit;",'race-'+first_action+'-cleanup.log')
   return {'first':first_action,'observed_wait':True,'second_code':expect,'request_rows':1,'audit_rows':1}
  races=[race('commit'),race('rollback')]
 after=execute("select country_code||':'||request_key||':'||greeting_text||':'||actor from e6_app.greeting_requests order by 1;",'business-after.log')
 assert before==after,'Unrelated business rows changed'
 session_after=execute("select 'SESSION_COUNT:'||count(*) from apex_workspace_sessions where workspace_name='E6_APP';",'sessions-after.log')
 assert session_before==session_after,'Native session leak'
 execute("declare n number; begin select count(*) into n from e6_app.greeting_requests where request_key in ('ALLOWED-ROLLBACK','BOB-ALLOWED','SESSION-DENY','FAIL-AUDIT'); if n<>0 then raise_application_error(-20485,'Leaked test requests'); end if; end;\n/",'no-partial-business.log')
 (OUT/'transaction-results.json').write_text(json.dumps({'races':races,'partial_failure':'rolled back only the operation','caller_rollback':'passed','unrelated_business_rows':'unchanged','session_creation_is_authentication':False},indent=2)+'\n')
 print('PASS native contexts, propagated init failure, caller rollback, partial failure and both controlled unique-key races')

if __name__=='__main__':{'unit':unit,'compatibility':compatibility,'integration':sessions_transactions}[sys.argv[1]]()
