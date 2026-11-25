"""Bounded real Oracle compatible expansion and interrupted catch-up experiment."""
import concurrent.futures,json,re,subprocess,time,sys,os
SCHEMA="E12_RUN_"+str(os.getpid())
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'progress/E.12/tests'
BASE=['podman','--connection','apex-cicd','exec','-i','--user','oracle','apex-db','bash','-lc','sqlplus -s / as sysdba']
PREFIX='''whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
set define off
set feedback off
set heading off
set pagesize 0
set serveroutput on
alter session set container=FREEPDB1;
set serveroutput on
'''
def sql(body,name):
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/(name+'.sql')).write_text(body)
    r=subprocess.run(BASE,input=PREFIX+"begin dbms_output.put_line(to_char(systimestamp,'YYYY-MM-DD HH24:MI:SS.FF')); end;\n/\n"+body.replace('e12_app',SCHEMA).replace('E12_APP',SCHEMA)+'\nprompt E12_COMPLETE\nexit\n',text=True,capture_output=True,timeout=180)
    out=r.stdout+r.stderr;OUT.mkdir(parents=True,exist_ok=True);(OUT/name).write_text(out)
    if r.returncode or re.search(r'(?m)^\s*(ORA-|PLS-|SP2-|Warning:)',out) or 'E12_COMPLETE' not in out:raise RuntimeError(out[-2500:])
    return out

def equal(source,target):
    if len(target)!=len({r[0] for r in target}) or sorted(source)!=sorted(target):raise ValueError('Missing, duplicated or stale changes')

def unit():
    equal([(1,'new'),(3,'insert')],[(3,'insert'),(1,'new')])
    for bad in [[(1,'old'),(3,'insert')],[(1,'new')],[(1,'new'),(3,'insert'),(3,'insert')]]:
        try:equal([(1,'new'),(3,'insert')],bad)
        except ValueError:pass
        else:raise AssertionError('Accepted corruption')
    print('PASS equality rejects stale, missing and duplicate rows; synthetic assertion checks only')

def integration():
    exists=sql("select count(*) from dba_users where username='E12_APP';",'inventory.log')
    if re.search(r'(?m)^\s*1\s*$',exists):
        sql("declare n number; begin select count(*) into n from e12_app.fixture_owner where marker='APEX_CICD_E12'; if n<>1 then raise_application_error(-20010,'foreign fixture'); end if; end;\n/\ndrop user e12_app cascade;",'reset-owned-fixture.log')
    sql('''create user e12_app no authentication quota 20m on users;
create table e12_app.component_version(version varchar2(20));
insert into e12_app.component_version values('1.0.0');
create table e12_app.fixture_owner(marker varchar2(30));
insert into e12_app.fixture_owner values('APEX_CICD_E12');
create table e12_app.history(id number primary key, message varchar2(100));
create table e12_app.settings(k varchar2(20) primary key,v varchar2(20));
insert into e12_app.settings values('language','en');
insert into e12_app.history values(1,'retained');
insert into e12_app.history values(2,'delete me');
create or replace package e12_app.foundation as
function greet(p_name varchar2) return varchar2;
procedure save(p_id number,p_name varchar2);
end;
/
create or replace package body e12_app.foundation as
function greet(p_name varchar2) return varchar2 is begin return 'Hello '||p_name; end;
procedure save(p_id number,p_name varchar2) is begin insert into e12_app.history(id,message) values(p_id,greet(p_name)); end;
end;
/
create or replace procedure e12_app.hello(p_id number) as n number; begin e12_app.foundation.save(p_id,'Hello'); select count(*) into n from e12_app.history where id=p_id; if n<>1 then raise_application_error(-20001,'missing Hello'); end if; end;
/
create or replace procedure e12_app.world(p_id number) as n number; begin e12_app.foundation.save(p_id,'World'); select count(*) into n from e12_app.history where id=p_id; if n<>1 then raise_application_error(-20001,'missing World'); end if; end;
/
commit;
''','baseline.log')
    def traffic(label,offset):
        commands=[]
        for i in range(1,121):
            commands.append(f"begin e12_app.{label}({offset+i}); commit; dbms_output.put_line('{label}:{i}:'||to_char(systimestamp,'HH24:MI:SS.FF')); end;\n/\nbegin dbms_session.sleep(.1); end;\n/")
        commands.append(f"begin dbms_output.put_line('{label}:120'); end;\n/")
        return sql('\n'.join(commands),label+'.log')
    legacy=sql("select text from dba_source where owner='E12_APP' and name in ('FOUNDATION','HELLO','WORLD') order by name,type,line;",'legacy-before.log').split('\n',1)[1]
    with concurrent.futures.ThreadPoolExecutor() as pool:
        hello=pool.submit(traffic,'hello',1000);world=pool.submit(traffic,'world',2000)
        time.sleep(1)
        sql('''alter table e12_app.history add(language varchar2(2));
create table e12_app.change_log(event_id number generated always as identity primary key,id number,op varchar2(1),actor varchar2(128));
create or replace trigger e12_app.capture_changes after insert or update or delete on e12_app.history for each row
begin
if deleting then insert into e12_app.change_log(id,op,actor) values(:old.id,'D',sys_context('USERENV','CLIENT_IDENTIFIER'));
elsif inserting then insert into e12_app.change_log(id,op,actor) values(:new.id,'I',sys_context('USERENV','CLIENT_IDENTIFIER'));
else insert into e12_app.change_log(id,op,actor) values(:new.id,'U',sys_context('USERENV','CLIENT_IDENTIFIER')); end if;
end;
/
create table e12_app.next_history as select id,message,language from e12_app.history where 1=0;
alter table e12_app.next_history add primary key(id);
insert into e12_app.next_history select * from e12_app.history;
commit;
create or replace function e12_app.greet_language(p_name varchar2,p_language varchar2 default 'en') return varchar2 as
begin if p_language='pl' then return 'Witaj '||p_name; elsif p_language='en' then return e12_app.foundation.greet(p_name); else raise_application_error(-20002,'unsupported language'); end if; end;
/
''','expand-backfill.log')
        sql("update e12_app.component_version set version='1.1.0';\ncommit;",'version.log')
        # Separate migration connection terminates with uncommitted stale update.
        r=subprocess.run(BASE,input=PREFIX+"update "+SCHEMA+".next_history set message='stale' where id=1;\nexit failure rollback\n",text=True,capture_output=True,timeout=30)
        (OUT/'interruption.log').write_text(r.stdout+r.stderr);assert r.returncode!=0
        sql("""begin dbms_session.set_identifier('E12_CONCURRENT'); end;
/
insert into e12_app.history(id,message,language) values(3,'concurrent insert','pl');
update e12_app.history set message='newer accepted' where id=1;
delete from e12_app.history where id=2;
commit;
""",'concurrent.log')
        time.sleep(1)
        sql('''lock table e12_app.history in share mode;
merge into e12_app.next_history t using e12_app.history s on(t.id=s.id)
when matched then update set t.message=s.message,t.language=s.language
when not matched then insert(id,message,language) values(s.id,s.message,s.language);
delete from e12_app.next_history t where not exists(select 1 from e12_app.history s where s.id=t.id);
declare n number; begin
select count(*) into n from ((select * from e12_app.history minus select * from e12_app.next_history) union all (select * from e12_app.next_history minus select * from e12_app.history));
if n<>0 then raise_application_error(-20003,'cutover mismatch'); end if;
dbms_output.put_line('CUTOVER_EQUAL');
end;
/
commit;
''','catchup.log')
        assert 'hello:120' in hello.result();assert 'world:120' in world.result()
    result=sql('''declare n number; s varchar2(100); begin
select count(*) into n from e12_app.history where id between 1001 and 1120 or id between 2001 and 2120;
if n<>240 then raise_application_error(-20004,'traffic lost'); end if;
select message into s from e12_app.history where id=1; if s<>'newer accepted' then raise_application_error(-20005,'overwritten'); end if;
select count(distinct op) into n from e12_app.change_log where actor='E12_CONCURRENT'; if n<>3 then raise_application_error(-20006,'missing attribution'); end if;
select count(*) into n from e12_app.settings where k='language' and v='en'; if n<>1 then raise_application_error(-20007,'settings lost'); end if;
if e12_app.greet_language('Jan','pl')<>'Witaj Jan' or e12_app.greet_language('Jan')<>'Hello Jan' then raise_application_error(-20008,'language'); end if;
e12_app.hello(3001); e12_app.world(3002);
select count(*) into n from dba_objects where owner='E12_APP' and status<>'VALID'; if n<>0 then raise_application_error(-20009,'invalid objects'); end if;
dbms_output.put_line('ASSERTIONS_PASS'); end;
/
''','assertions.log')
    assert 'ASSERTIONS_PASS' in result
    after=sql("select text from dba_source where owner='E12_APP' and name in ('FOUNDATION','HELLO','WORLD') order by name,type,line;",'legacy-after.log').split('\n',1)[1]
    assert legacy==after,'Legacy source changed'
    try:
        sql("select e12_app.greet_language('Jan','xx') from dual;",'unsupported-language.log')
    except RuntimeError as exc:
        assert 'ORA-20002' in str(exc)
    else:raise AssertionError('Unsupported language accepted')
    (OUT/'experiment.json').write_text(json.dumps({'legacy_writes':240,'legacy_errors':0,'cutover_equal':True,'capture_operations':['I','U','D'],'interrupted_transaction_rolled_back':True,'schema':SCHEMA,'limits':'Finite PL/SQL workload, no APEX browser or production deployment claim'},indent=2))
    print('PASS real Oracle expansion, 240 unchanged consumer transactions, interrupted migration and exact locked cutover')
if __name__=='__main__':
    {'unit':unit,'integration':integration}[sys.argv[1]]()
