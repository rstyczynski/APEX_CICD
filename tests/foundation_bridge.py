"""E.13 isolated real Oracle compatibility bridge experiment."""
import concurrent.futures
import hashlib
import json
import os
import subprocess
from pathlib import Path
import sys
import time
import foundation_lab as db
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'progress/E.13/tests'/('run_'+str(os.getpid()))
db.OUT=OUT
db.SCHEMA='E13_RUN_'+str(os.getpid())
def sql(source,name):
    return db.sql(source,name)
def unit():
    db.unit()
def integration():
    sql('''create user e12_app no authentication quota 20m on users;
create table e12_app.history(id number primary key,message varchar2(100));
create table e12_app.details(id number primary key references e12_app.history(id),template varchar2(20),person varchar2(80));
create table e12_app.settings(k varchar2(20),v varchar2(20));
insert into e12_app.settings values('language','en');
insert into e12_app.history values(0,'retained greeting');
insert into e12_app.details values(0,'literal','retained greeting');
create table e12_app.callers(component varchar2(20) primary key,api number);
insert into e12_app.callers values('Hello',1);
insert into e12_app.callers values('World',1);
create table e12_app.lifecycle(legacy_enabled number);
insert into e12_app.lifecycle values(1);
commit;
create or replace package e12_app.bridge as
procedure legacy_write(i number,msg varchar2,inject_failure boolean default false);
procedure template_write(i number,template varchar2,parameters sys.odcivarchar2list,inject_failure boolean default false);
function read_message(i number) return varchar2;
procedure retire;
end;
/
create or replace package body e12_app.bridge as
procedure paired(i number,msg varchar2,t varchar2,p varchar2,f boolean) is begin
savepoint bridge_call;
insert into e12_app.history values(i,msg);
if f then raise_application_error(-20101,'injected between writes'); end if;
insert into e12_app.details values(i,t,p);
exception when others then rollback to bridge_call; raise;
end;
procedure legacy_write(i number,msg varchar2,inject_failure boolean default false) is n number; begin
select legacy_enabled into n from e12_app.lifecycle;
if n<>1 then raise_application_error(-20102,'legacy retired'); end if;
paired(i,msg,'literal',msg,inject_failure);
end;
procedure template_write(i number,template varchar2,parameters sys.odcivarchar2list,inject_failure boolean default false) is begin
if template<>'greeting' or template is null or parameters.count<>1 then raise_application_error(-20103,'template and one name required'); end if;
if parameters(1) is null then raise_application_error(-20103,'name required'); end if;
paired(i,'Hello '||parameters(1),template,parameters(1),inject_failure);
end;
function read_message(i number) return varchar2 is s varchar2(100); begin select message into s from e12_app.history where id=i; return s; end;
procedure retire is n number; begin
lock table e12_app.callers in exclusive mode;
select count(*) into n from e12_app.callers where api=1;
if n<>0 then raise_application_error(-20104,'legacy callers remain'); end if;
update e12_app.lifecycle set legacy_enabled=0;
end;
end;
/
create or replace procedure e12_app.hello(i number) is s varchar2(100); n number; begin
select api into n from e12_app.callers where component='Hello';
if n=1 then e12_app.bridge.legacy_write(i,'Hello Hello'); else e12_app.bridge.template_write(i,'greeting',sys.odcivarchar2list('Hello')); end if;
s:=e12_app.bridge.read_message(i); if s<>'Hello Hello' then raise_application_error(-20105,'Hello visibility'); end if;
end;
/
create or replace procedure e12_app.world(i number) is s varchar2(100); n number; begin
select api into n from e12_app.callers where component='World';
if n=1 then e12_app.bridge.legacy_write(i,'Hello World'); else e12_app.bridge.template_write(i,'greeting',sys.odcivarchar2list('World')); end if;
s:=e12_app.bridge.read_message(i); if s<>'Hello World' then raise_application_error(-20105,'World visibility'); end if;
end;
/
declare n number; begin select count(*) into n from dba_objects where owner='E12_APP' and status<>'VALID'; if n<>0 then raise_application_error(-20110,'invalid objects'); end if; end;
/
''','setup.log')
    sql('''begin
begin e12_app.bridge.template_write(99,'greeting',sys.odcivarchar2list('Failure'),true); raise_application_error(-20120,'failure not injected');
exception when others then if sqlcode<>-20101 then raise; end if; end;
commit;
end;
/
declare n number; begin select count(*) into n from e12_app.history where id=99; if n<>0 then raise_application_error(-20121,'partial history'); end if;
select count(*) into n from e12_app.details where id=99; if n<>0 then raise_application_error(-20121,'partial details'); end if;
dbms_output.put_line('CAUGHT_FAILURE_COMMIT_ATOMIC'); end;
/
update e12_app.callers set api=2 where component='Hello';
commit;
''','failure-recovery.log')
    interrupted=subprocess.run(db.BASE,input=db.PREFIX+f"insert into {db.SCHEMA}.history values(98,'interrupted');\nprompt INTERRUPTED_BEFORE_COMPANION\nexit failure rollback\n",text=True,capture_output=True,timeout=30)
    (OUT/'interruption.log').write_text(interrupted.stdout+interrupted.stderr+f'PROCESS_EXIT={interrupted.returncode}\n')
    assert interrupted.returncode != 0
    sql("declare n number; begin select count(*) into n from e12_app.history where id=98; if n<>0 then raise_application_error(-20131,'interruption leaked'); end if; dbms_output.put_line('SESSION_INTERRUPTION_ROLLBACK_PASS'); end;\n/",'interruption-check.log')
    def traffic(component,offset):
        source=''
        for i in range(80):
            source+=f"begin e12_app.{component}({offset+i}); commit; dbms_output.put_line('{component}:{i}:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;\n/\n"
        return sql(source,component+'.log')
    with concurrent.futures.ThreadPoolExecutor() as pool:
        h=pool.submit(traffic,'hello',1000);w=pool.submit(traffic,'world',2000)
        assert 'hello:79:' in h.result();assert 'world:79:' in w.result()
    sql('''declare n number; begin
select count(*) into n from e12_app.history where id between 1000 and 1079 or id between 2000 and 2079;
if n<>160 then raise_application_error(-20122,'lost traffic'); end if;
select count(*) into n from e12_app.history h full outer join e12_app.details d on h.id=d.id where h.id is null or d.id is null or h.message<>case when d.template='literal' then d.person else 'Hello '||d.person end;
if n<>0 then raise_application_error(-20123,'visibility mismatch'); end if;
if e12_app.bridge.read_message(1000)<>'Hello Hello' or e12_app.bridge.read_message(2000)<>'Hello World' then raise_application_error(-20124,'shared visibility'); end if;
begin e12_app.bridge.retire; raise_application_error(-20125,'early retirement accepted'); exception when others then if sqlcode<>-20104 then raise; end if; end;
dbms_output.put_line('MIXED_READ_WRITE_AND_RETIREMENT_GUARD_PASS'); end;
/
update e12_app.callers set api=1 where component='Hello';
commit;
begin e12_app.hello(3000); e12_app.world(3001); commit; end;
/
declare n number; begin
if e12_app.bridge.read_message(1000)<>'Hello Hello' then raise_application_error(-20126,'new write lost on return'); end if;
select count(*) into n from e12_app.settings where k='language' and v='en'; if n<>1 then raise_application_error(-20127,'settings lost'); end if;
if e12_app.bridge.read_message(0)<>'retained greeting' then raise_application_error(-20128,'history lost'); end if;
dbms_output.put_line('RETURN_AFTER_NEW_WRITES_PRESERVATION_PASS'); end;
/
update e12_app.callers set api=2;
commit;
begin e12_app.bridge.retire; commit; end;
/
begin
begin e12_app.bridge.legacy_write(4000,'retired'); raise_application_error(-20129,'legacy accepted'); exception when others then if sqlcode<>-20102 then raise; end if; end;
e12_app.hello(4001); e12_app.world(4002); commit;
begin e12_app.bridge.template_write(4003,'unknown',sys.odcivarchar2list('x')); raise_application_error(-20130,'bad template accepted'); exception when others then if sqlcode<>-20103 then raise; end if; end;
dbms_output.put_line('RETIREMENT_AND_NEW_CONTRACT_PASS'); end;
/
''','assertions.log')
    (OUT/'receipt.json').write_text(json.dumps({'schema':db.SCHEMA,'driver_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'mixed_writes':160,'errors':0,'limits':'isolated PL/SQL finite experiment; no production or APEX rollout'},indent=2))
    print('PASS real Oracle bridge failure recovery, mixed traffic, legacy return and retirement',OUT)
if __name__=='__main__':
    {'unit':unit,'integration':integration}[sys.argv[1]]()
