# E.13 increment walkthrough

## Goal and starting state — slides 1–5

Validate [PBI-082](../../BACKLOG.md#pbi-082-validate-dual-write-failure-and-mixed-version-data-visibility) before [PBI-049](../../BACKLOG.md#pbi-049-prove-an-available-breaking-foundation-transition). [PLAN](../../PLAN.md) owns assignment; [design](sprint_E.13_design.md) owns mechanism choices; [tests](sprint_E.13_tests.md) owns measured outcomes. This is an isolated real Oracle PL/SQL experiment, following the compatible [E.12 experiment](../E.12/sprint_E.12_increment_demo.md), rather than the E.14 in-place maintenance-window experiment. The result is a reproducible bridge hypothesis with explicit return and retirement boundaries.

Prerequisites: repository checkout, Python 3, Podman with prepared `apex-cicd` connection, running `apex-db` with FREEPDB1, Oracle SQLPlus inside the database container. No credentials are printed or copied. SQLPlus uses the prepared local OS-authenticated database administrator to create only a unique E13_RUN_<process-id> schema. Keep this schema for inspection; never drop unrelated schemas. No native SQLcl PROJECT processing is performed by this experiment.

## Explain the driver before invocation — slides 4, 6–9

[foundation_bridge.py](../../tests/foundation_bridge.py) reuses the [SQL execution boundary](../../tests/foundation_lab.py) with its output redirected to this sprint. It runs SQLPlus in the real database container, selects FREEPDB1, enables failure-on-SQL-error and records every SQL/log. A 180-second subprocess deadline rejects a hung call. The template accepts one structured name in SYS.ODCIVARCHAR2LIST and rejects unknown templates. Both APIs enter a common savepoint; failure rolls back both writes without rolling back earlier caller work. History stores rendered messages, so legacy readers can see new writes. The registry is an explicit laboratory routing mechanism, not production caller discovery or identity enforcement.

The following complete constant SQL blocks run in driver order (schema placeholder `e12_app` is replaced with the unique E13_RUN name by the reused boundary). Wrapper SQL sets FREEPDB1, DEFINE OFF, SERVEROUTPUT ON and WHENEVER SQLERROR/OSERROR EXIT FAILURE ROLLBACK. These EXIT directives terminate the child SQLPlus process, never the reader's shell.

### SQLPlus wrapper

Every source block is sent through this complete prefix. The boundary also prints a timestamp, appends E12_COMPLETE as a completion sentinel and exits the child process; the historical sentinel name is a reused boundary marker, not an E.12 result.

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
begin dbms_output.put_line(to_char(systimestamp,'YYYY-MM-DD HH24:MI:SS.FF')); end;
/
-- per-stage body follows here
prompt E12_COMPLETE
exit
```

### SQL stage 1

```sql
create user e12_app no authentication quota 20m on users;
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
```

### SQL stage 2

```sql
begin
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
```

### SQL stage 3

```sql
declare n number; begin select count(*) into n from e12_app.history where id=98; if n<>0 then raise_application_error(-20131,'interruption leaked'); end if; dbms_output.put_line('SESSION_INTERRUPTION_ROLLBACK_PASS'); end;
/
```

### SQL stage 4

```sql
declare n number; begin
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
```

### Interrupted child and traffic SQL

The interrupted child inserts one uncommitted row and terminates SQLPlus with failure and rollback before its companion insert. The subsequent independent query verifies absence. This tests transactional session interruption; it does not simulate an operating-system crash.

```sql
insert into E13_RUN_<pid>.history values(98,'interrupted');
prompt INTERRUPTED_BEFORE_COMPANION
exit failure rollback
```

The driver generates 80 separate committed calls per consumer, replacing `<consumer>` with hello/world and `<id>` with 1000–1079 / 2000–2079. Each procedure performs its own read-back; two concurrent SQLPlus sessions execute these statements. The sleep spreads the finite sample; it is not a latency target.

```sql
begin
  E13_RUN_<pid>.<consumer>(<id>);
  commit;
  dbms_output.put_line('<consumer>:<index>:'||to_char(systimestamp,'HH24:MI:SS.FF'));
  dbms_session.sleep(.05);
end;
/
```

## 1. Verify prepared infrastructure — slide 6

Position the named shell session at the checkout root, then inspect the running containers. This read-only Podman query must show apex-db running. It does not start or reset infrastructure.

```bash
cd "$(git rev-parse --show-toplevel)"
podman --connection apex-cicd ps
```

## 2. Run the complete journey — slides 6–9

The driver explained above creates its unique schema, injects and verifies partial-write failure before migration, migrates Hello, executes mixed traffic, returns Hello to legacy, preserves new history/settings, migrates both and exercises guarded retirement. An exception/nonzero exit fails the run; no failed assertion may be treated as successful recovery. Run in the same shell:

```bash
python3 tests/foundation_bridge.py integration
```

Expected visible final output: `PASS real Oracle bridge failure recovery, mixed traffic, legacy return and retirement` followed by this run's evidence directory. That line is supported by individual SQL assertions, not a simulator.

## 3. Inspect intermediate and final results — slides 7–10

The following Python inspection reads the newest saved run's actual logs. Check failure rollback, independent session rollback, both 80-call streams and the return/retirement assertions. Open the directory with `code progress/E.13/tests` when the optional VS Code command is available; editor opening is not a database verification step.

```bash
python3 - <<'INSPECT'
from pathlib import Path
runs=sorted(Path('progress/E.13/tests').glob('run_*'),key=lambda p:p.stat().st_mtime)
runs=[p for p in runs if (p/'receipt.json').exists()]
p=runs[-1]
for name in ['failure-recovery.log','interruption.log','interruption-check.log','hello.log','world.log','assertions.log','receipt.json']:
    print('\n'+name+'\n'+(p/name).read_text())
INSPECT
```

The caught-error marker confirms no partial row survives even after caller commit. The interruption log has a nonzero child exit, followed by SESSION_INTERRUPTION_ROLLBACK_PASS. Mixed stream logs show index 0 through 79. Assertions report MIXED_READ_WRITE_AND_RETIREMENT_GUARD_PASS, RETURN_AFTER_NEW_WRITES_PRESERVATION_PASS and RETIREMENT_AND_NEW_CONTRACT_PASS. A legacy request after retirement is deliberately rejected; the exception is checked by its specific Oracle error, then both new consumers still succeed.

## Outcomes, failure limits and next decisions — slides 10–13

PBI-082 and PBI-049 claims require the real integration assertions and current [requirement checklist](sprint_E.13_remaining_work.md). Full regression is separate; inspect the [test report](sprint_E.13_tests.md). No production zero-downtime bound, APEX browser journey, unregistered external caller discovery, or E.14 maintenance windows are established. Return to legacy is supported before retirement because rendered text is retained; it does not recreate arbitrary text into a structured name. After retirement, restoring legacy is outside this tested journey.

On SQL/connectivity failure, retain the failing log, diagnose the prepared connection/container and retry in a new schema. The driver does not reuse a failed schema or silently reset business data. A successful fresh run proves its own outcome, never changes a prior failure into success. No failed bridge hypothesis was observed in the current bounded experiment. [Manual](user_manual.md) owns recovery and [handover](sprint_E.13_handover.md) records live operations and review. The matching [presentation](sprint_E.13_increment_demo.pptx) uses the slide map above.
