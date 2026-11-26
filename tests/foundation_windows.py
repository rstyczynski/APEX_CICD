"""Real Oracle component maintenance windows on the qualified bridge fixture."""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import foundation_bridge as bridge
import foundation_lab as db
OUT=Path(__file__).resolve().parents[1]/'progress/E.14/tests'/('run_'+str(os.getpid()))
bridge.OUT=OUT
db.OUT=OUT
db.SCHEMA='E14_RUN_'+str(os.getpid())
def sql(body,name):
    return db.sql(body.replace('; commit;', ';\ncommit;').replace('; insert into', ';\ninsert into'),name)
def state(routes):
    if set(routes)!= {'Hello','World'} or any(v not in (1,2) for v in routes.values()):
        raise ValueError('invalid routes')
def unit():
    state({'Hello':1,'World':2})
    for bad in ({'Hello':2},{'Hello':3,'World':1}):
        try: state(bad)
        except ValueError: pass
        else: raise AssertionError('accepted invalid routes')
    print('PASS synthetic route validation only')
def integration():
    # Reuse actual setup SQL without replaying the E.13 migration journey.
    import ast
    tree=ast.parse(Path(bridge.__file__).read_text())
    fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='integration')
    setup=ast.literal_eval(fn.body[0].value.args[0])
    sql(setup,'setup.log')
    sql('''alter table e12_app.callers add(maintenance number default 0);
create table e12_app.migrations(component varchar2(20),phase varchar2(20));
create or replace procedure e12_app.request(c varchar2,i number) is m number; begin
select maintenance into m from e12_app.callers where component=c;
if m=1 then raise_application_error(-20201,'component maintenance'); end if;
if c='Hello' then e12_app.hello(i); elsif c='World' then e12_app.world(i); else raise_application_error(-20202,'unknown component'); end if;
end;
/
''','window-setup.log')
    def traffic(c,offset):
        return sql(''.join(f"begin e12_app.request('{c}',{offset+i}); commit; dbms_output.put_line('TRAFFIC:{c}:{i}:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;\n/\n" for i in range(80)),c+'-traffic.log')
    for component,other,offset in [('Hello','World',1000),('World','Hello',2000)]:
        sql(f"update e12_app.callers set maintenance=1 where component='{component}'; commit;",component+'-start.log')
        with concurrent.futures.ThreadPoolExecutor() as pool:
            live=pool.submit(traffic,other,offset)
            sql(f"begin begin e12_app.request('{component}',9999); raise_application_error(-20203,'maintenance bypass'); exception when others then if sqlcode<>-20201 then raise; end if; end; end;\n/",component+'-reject.log')
            body=f"update {db.SCHEMA}.callers set api=2 where component='{component}';\ninsert into {db.SCHEMA}.migrations values('{component}','partial');\nprompt INTERRUPTED\nexit failure rollback\n"
            r=subprocess.run(db.BASE,input=db.PREFIX+body,text=True,capture_output=True,timeout=30)
            (OUT/(component+'-interruption.log')).write_text(r.stdout+r.stderr+f'EXIT={r.returncode}\n')
            assert r.returncode!=0 and 'INTERRUPTED' in r.stdout
            sql(f"declare n number; begin select api into n from e12_app.callers where component='{component}'; if n<>1 then raise_application_error(-20204,'route leaked'); end if; select count(*) into n from e12_app.migrations where component='{component}'; if n<>0 then raise_application_error(-20205,'journal leaked'); end if; dbms_output.put_line('RECOVERY_PASS'); end;\n/\nbegin dbms_session.sleep(1); end;\n/",component+'-recovery.log')
            assert f'TRAFFIC:{other}:79:' in live.result()
        sql(f"update e12_app.callers set api=2,maintenance=0 where component='{component}'; insert into e12_app.migrations values('{component}','complete'); commit;\nbegin e12_app.request('{component}',{offset+500}); commit; end;\n/",component+'-complete.log')
    sql('''declare n number; begin
select count(*) into n from e12_app.callers where api=2 and maintenance=0; if n<>2 then raise_application_error(-20206,'routes incomplete'); end if;
select count(*) into n from e12_app.history; if n<>163 then raise_application_error(-20207,'history lost'); end if;
select count(*) into n from e12_app.history h full outer join e12_app.details d on h.id=d.id where h.id is null or d.id is null or h.message<>case when d.template='literal' then d.person else 'Hello '||d.person end; if n<>0 then raise_application_error(-20208,'representation mismatch'); end if;
select count(*) into n from e12_app.settings where k='language' and v='en'; if n<>1 then raise_application_error(-20209,'configuration lost'); end if;
if e12_app.bridge.read_message(0)<>'retained greeting' then raise_application_error(-20210,'baseline lost'); end if;
dbms_output.put_line('COMPONENT_WINDOWS_PRESERVATION_PASS'); end;
/
''','assertions.log')
    (OUT/'receipt.json').write_text(json.dumps({'schema':db.SCHEMA,'driver_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'unaffected_commits':160,'result':'PASS','limits':'finite isolated PL/SQL experiment; no production APEX rollout'},indent=2))
    print('PASS real Oracle separate windows and interrupted component recovery',OUT)
if __name__=='__main__': {'unit':unit,'integration':integration}[sys.argv[1]]()
