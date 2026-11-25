# E.12 increment walkthrough

## Goal, starting state and scope (slides 1–4)

Prove the compatible language extension and interrupted catch-up with real writes. [Backlog](../../BACKLOG.md) PBI-048 and PBI-081 own acceptance, [design](sprint_E.12_design.md) owns the bounded experiment, and [test record](sprint_E.12_tests.md) owns results. [Manual](user_manual.md) owns operating prerequisites. The [deck](sprint_E.12_increment_demo.pptx) accompanies this complete sequence.

## 1. Establish the environment (slide 5)

Use the prepared local Podman service, running apex-db Oracle container, Python 3 and Git. OS authentication requires permission to execute SQLPlus as oracle. VS Code's code command must be on PATH to open files. No database passwords are required. Each run creates its own E12_RUN schema and retains it for inspection; it does not reset an existing application. It consumes small USERS tablespace space. This is a database experiment; browser steps and SQLcl PROJECT packaging do not apply. No project metadata or approved SQLcl version is modified.

```bash
cd "$(git rev-parse --show-toplevel)"
podman --connection apex-cicd version
```

Expected: client and server version details, with no connection failure.

## 2. Understand the experiment before running (slide 6)

The Python driver invokes SQLPlus over podman exec with strict Oracle error detection, completion markers and bounded subprocess timeouts. The baseline creates history/settings, the legacy Foundation specification/body and unchanged Hello/World procedures. Two separate clients perform 120 individual committed calls each with pauses between calls. The upgrade adds nullable language storage, a journal trigger and a separate optional-language function, preserving the legacy package. A first backfill commits. A separate migration transaction deliberately exits with rollback. Attributable legacy insert/update/delete operations commit while consumers continue. Catch-up takes a short shared source lock, merges current source and removes target rows deleted at source, then compares both complete sets before committing. The lock can delay writers; no maximum latency guarantee is claimed. This is a reconciliation experiment, not a dual-write bridge or production migration controller.

The complete SQL string sources used by the driver follow. The driver substitutes its unique schema name for e12_app. Traffic call IDs and labels are generated in the Python source; the full driver is linked [here](../../tests/foundation_lab.py). SQLPlus configuration disables substitution and enables server output. SQL errors roll back and fail; committed migration stages remain available for inspection. Rerunning creates a new unique fixture rather than assuming a failed schema is safe to reuse.

```sql
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
set define off
set feedback off
set heading off
set pagesize 0
set serveroutput on
alter session set container=FREEPDB1;
set serveroutput on
```

```sql
create user e12_app no authentication quota 20m on users;
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
```

```sql
declare n number; s varchar2(100); begin
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
```

```sql
declare n number; begin select count(*) into n from e12_app.fixture_owner where marker='APEX_CICD_E12'; if n<>1 then raise_application_error(-20010,'foreign fixture'); end if; end;
/
drop user e12_app cascade;
```

```sql
alter table e12_app.history add(language varchar2(2));
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
```

```sql
begin dbms_session.set_identifier('E12_CONCURRENT'); end;
/
insert into e12_app.history(id,message,language) values(3,'concurrent insert','pl');
update e12_app.history set message='newer accepted' where id=1;
delete from e12_app.history where id=2;
commit;
```

```sql
lock table e12_app.history in share mode;
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
```

## 3. Run and inspect the actual journey (slides 6–9)

The invocation runs the explained sequence against the real database. It is safe to repeat with a new schema, subject to available database space.

```bash
python3 tests/foundation_lab.py integration
code progress/E.12/tests/experiment.json
code progress/E.12/tests/hello.log
code progress/E.12/tests/world.log
code progress/E.12/tests/expand-backfill.log
code progress/E.12/tests/concurrent.log
code progress/E.12/tests/catchup.log
code progress/E.12/tests/assertions.log
```

Expected: PASS for 240 accepted unchanged-consumer writes; ASSERTIONS_PASS; CUTOVER_EQUAL; exact schema identity in experiment.json. Inspect both clients' timestamps against expansion and catch-up times. Read the source/target assertions: they establish equality at the locked boundary, not automatic replication of later writes. The retained original ID 1 has the intentionally updated value newer accepted; ID 2 is intentionally deleted; ID 3 is the attributed insertion. Language checks require Hello Jan for omitted language and Witaj Jan for Polish. The setting language=en survives.

## 4. Inspect failure and recovery (slides 10–12)

interruption.log records the deliberate rollback exit, followed by concurrent.log and catchup.log. It interrupts one migration transaction after the first backfill is committed; it does not kill the Oracle service. The early attempts exposed hidden SQLPlus output and dependencies held by a long loop. Separate SQLPlus settings and separately committed client calls corrected those test defects. Shared schema resets collided with another execution; fixtures now use unique names. Historical failures remain failures.

Unsupported language raises an Oracle application error. Unknown infrastructure errors fail the run. No browser behavior, production deployment, E.13 bridge or E.14 component windows are established. Review the [current tests](sprint_E.12_tests.md) and [handover](sprint_E.12_handover.md) before deciding completion.
