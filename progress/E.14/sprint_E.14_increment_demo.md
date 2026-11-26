# E.14 increment demonstration

## Goal and starting state — slides 1–4

The operator will migrate Hello and World in separate windows and inspect interrupted-migration recovery. [PLAN](../../PLAN.md) assigns PBI-050 and PBI-080; [design](sprint_E.14_design.md) defines the bounded fixture. Use the already prepared Podman connection apex-cicd and running apex-db container, Oracle FREEPDB1 and SQLPlus. Python 3 and Bash must be available. No credential or settings file is created. These are backend laboratory procedures; no browser action is claimed. Both consumers initially use the legacy bridge, with retained greeting and English configuration.

## 1. Inspect prerequisites — slide 6

The Podman command inspects running containers through the prepared connection. It changes no application data. Confirm apex-db is running before proceeding.

```bash
cd "$(git rev-parse --show-toplevel)"
podman --connection apex-cicd ps
```

## 2. Understand the experiment — slides 4–12

The Python driver extracts E.13 setup SQL through Python syntax-tree inspection, creates a uniquely named no-authentication Oracle fixture schema and preserves it through both windows. SQLPlus uses the prepared container SYS connection and switches to FREEPDB1. All statements and outputs are retained in the printed run directory. Legacy arbitrary-text and new template/name calls share a savepoint-protected bridge; each request reads back its result. Maintenance is a per-component registry flag. The migrating component rejects specifically with -20201; the other executes 80 committed calls in an independent SQLPlus session. Before commit, a child session exits with failure and rollback. Independent SQL verifies the route and journal were rolled back. Retry atomically commits the route/journal, then re-enables that component. Final assertions require 163 historical rows, paired representation equality, retained baseline greeting/settings and both routes on the new contract.

### Complete SQL before invocation

The following is the complete SQL from the verified direct run, in execution-stage order. The driver substitutes the unique schema for e12_app and adds SQLPlus fail-on-error, server-output and FREEPDB1 context. Traffic files contain the full bounded sample; interruption statements are passed to a separate child session ending in failure rollback. The child failure is expected only when its marker is present and the independent recovery assertions pass.


### setup.log.sql

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

### window-setup.log.sql

```sql
alter table e12_app.callers add(maintenance number default 0);
create table e12_app.migrations(component varchar2(20),phase varchar2(20));
create or replace procedure e12_app.request(c varchar2,i number) is m number; begin
select maintenance into m from e12_app.callers where component=c;
if m=1 then raise_application_error(-20201,'component maintenance'); end if;
if c='Hello' then e12_app.hello(i); elsif c='World' then e12_app.world(i); else raise_application_error(-20202,'unknown component'); end if;
end;
/

```

### Hello-start.log.sql

```sql
update e12_app.callers set maintenance=1 where component='Hello';
commit;
```

### Hello-reject.log.sql

```sql
begin begin e12_app.request('Hello',9999); raise_application_error(-20203,'maintenance bypass'); exception when others then if sqlcode<>-20201 then raise; end if; end; end;
/
```

### Hello-recovery.log.sql

```sql
declare n number; begin select api into n from e12_app.callers where component='Hello'; if n<>1 then raise_application_error(-20204,'route leaked'); end if; select count(*) into n from e12_app.migrations where component='Hello'; if n<>0 then raise_application_error(-20205,'journal leaked'); end if; dbms_output.put_line('RECOVERY_PASS'); end;
/
begin dbms_session.sleep(1); end;
/
```

### World-traffic.log.sql

```sql
begin e12_app.request('World',1000);
commit; dbms_output.put_line('TRAFFIC:World:0:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1001);
commit; dbms_output.put_line('TRAFFIC:World:1:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1002);
commit; dbms_output.put_line('TRAFFIC:World:2:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1003);
commit; dbms_output.put_line('TRAFFIC:World:3:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1004);
commit; dbms_output.put_line('TRAFFIC:World:4:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1005);
commit; dbms_output.put_line('TRAFFIC:World:5:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1006);
commit; dbms_output.put_line('TRAFFIC:World:6:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1007);
commit; dbms_output.put_line('TRAFFIC:World:7:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1008);
commit; dbms_output.put_line('TRAFFIC:World:8:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1009);
commit; dbms_output.put_line('TRAFFIC:World:9:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1010);
commit; dbms_output.put_line('TRAFFIC:World:10:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1011);
commit; dbms_output.put_line('TRAFFIC:World:11:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1012);
commit; dbms_output.put_line('TRAFFIC:World:12:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1013);
commit; dbms_output.put_line('TRAFFIC:World:13:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1014);
commit; dbms_output.put_line('TRAFFIC:World:14:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1015);
commit; dbms_output.put_line('TRAFFIC:World:15:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1016);
commit; dbms_output.put_line('TRAFFIC:World:16:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1017);
commit; dbms_output.put_line('TRAFFIC:World:17:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1018);
commit; dbms_output.put_line('TRAFFIC:World:18:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1019);
commit; dbms_output.put_line('TRAFFIC:World:19:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1020);
commit; dbms_output.put_line('TRAFFIC:World:20:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1021);
commit; dbms_output.put_line('TRAFFIC:World:21:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1022);
commit; dbms_output.put_line('TRAFFIC:World:22:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1023);
commit; dbms_output.put_line('TRAFFIC:World:23:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1024);
commit; dbms_output.put_line('TRAFFIC:World:24:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1025);
commit; dbms_output.put_line('TRAFFIC:World:25:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1026);
commit; dbms_output.put_line('TRAFFIC:World:26:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1027);
commit; dbms_output.put_line('TRAFFIC:World:27:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1028);
commit; dbms_output.put_line('TRAFFIC:World:28:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1029);
commit; dbms_output.put_line('TRAFFIC:World:29:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1030);
commit; dbms_output.put_line('TRAFFIC:World:30:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1031);
commit; dbms_output.put_line('TRAFFIC:World:31:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1032);
commit; dbms_output.put_line('TRAFFIC:World:32:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1033);
commit; dbms_output.put_line('TRAFFIC:World:33:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1034);
commit; dbms_output.put_line('TRAFFIC:World:34:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1035);
commit; dbms_output.put_line('TRAFFIC:World:35:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1036);
commit; dbms_output.put_line('TRAFFIC:World:36:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1037);
commit; dbms_output.put_line('TRAFFIC:World:37:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1038);
commit; dbms_output.put_line('TRAFFIC:World:38:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1039);
commit; dbms_output.put_line('TRAFFIC:World:39:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1040);
commit; dbms_output.put_line('TRAFFIC:World:40:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1041);
commit; dbms_output.put_line('TRAFFIC:World:41:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1042);
commit; dbms_output.put_line('TRAFFIC:World:42:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1043);
commit; dbms_output.put_line('TRAFFIC:World:43:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1044);
commit; dbms_output.put_line('TRAFFIC:World:44:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1045);
commit; dbms_output.put_line('TRAFFIC:World:45:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1046);
commit; dbms_output.put_line('TRAFFIC:World:46:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1047);
commit; dbms_output.put_line('TRAFFIC:World:47:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1048);
commit; dbms_output.put_line('TRAFFIC:World:48:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1049);
commit; dbms_output.put_line('TRAFFIC:World:49:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1050);
commit; dbms_output.put_line('TRAFFIC:World:50:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1051);
commit; dbms_output.put_line('TRAFFIC:World:51:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1052);
commit; dbms_output.put_line('TRAFFIC:World:52:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1053);
commit; dbms_output.put_line('TRAFFIC:World:53:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1054);
commit; dbms_output.put_line('TRAFFIC:World:54:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1055);
commit; dbms_output.put_line('TRAFFIC:World:55:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1056);
commit; dbms_output.put_line('TRAFFIC:World:56:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1057);
commit; dbms_output.put_line('TRAFFIC:World:57:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1058);
commit; dbms_output.put_line('TRAFFIC:World:58:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1059);
commit; dbms_output.put_line('TRAFFIC:World:59:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1060);
commit; dbms_output.put_line('TRAFFIC:World:60:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1061);
commit; dbms_output.put_line('TRAFFIC:World:61:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1062);
commit; dbms_output.put_line('TRAFFIC:World:62:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1063);
commit; dbms_output.put_line('TRAFFIC:World:63:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1064);
commit; dbms_output.put_line('TRAFFIC:World:64:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1065);
commit; dbms_output.put_line('TRAFFIC:World:65:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1066);
commit; dbms_output.put_line('TRAFFIC:World:66:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1067);
commit; dbms_output.put_line('TRAFFIC:World:67:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1068);
commit; dbms_output.put_line('TRAFFIC:World:68:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1069);
commit; dbms_output.put_line('TRAFFIC:World:69:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1070);
commit; dbms_output.put_line('TRAFFIC:World:70:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1071);
commit; dbms_output.put_line('TRAFFIC:World:71:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1072);
commit; dbms_output.put_line('TRAFFIC:World:72:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1073);
commit; dbms_output.put_line('TRAFFIC:World:73:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1074);
commit; dbms_output.put_line('TRAFFIC:World:74:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1075);
commit; dbms_output.put_line('TRAFFIC:World:75:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1076);
commit; dbms_output.put_line('TRAFFIC:World:76:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1077);
commit; dbms_output.put_line('TRAFFIC:World:77:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1078);
commit; dbms_output.put_line('TRAFFIC:World:78:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('World',1079);
commit; dbms_output.put_line('TRAFFIC:World:79:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/

```

### Hello-complete.log.sql

```sql
update e12_app.callers set api=2,maintenance=0 where component='Hello';
insert into e12_app.migrations values('Hello','complete');
commit;
begin e12_app.request('Hello',1500);
commit; end;
/
```

### World-start.log.sql

```sql
update e12_app.callers set maintenance=1 where component='World';
commit;
```

### World-reject.log.sql

```sql
begin begin e12_app.request('World',9999); raise_application_error(-20203,'maintenance bypass'); exception when others then if sqlcode<>-20201 then raise; end if; end; end;
/
```

### World-recovery.log.sql

```sql
declare n number; begin select api into n from e12_app.callers where component='World'; if n<>1 then raise_application_error(-20204,'route leaked'); end if; select count(*) into n from e12_app.migrations where component='World'; if n<>0 then raise_application_error(-20205,'journal leaked'); end if; dbms_output.put_line('RECOVERY_PASS'); end;
/
begin dbms_session.sleep(1); end;
/
```

### Hello-traffic.log.sql

```sql
begin e12_app.request('Hello',2000);
commit; dbms_output.put_line('TRAFFIC:Hello:0:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2001);
commit; dbms_output.put_line('TRAFFIC:Hello:1:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2002);
commit; dbms_output.put_line('TRAFFIC:Hello:2:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2003);
commit; dbms_output.put_line('TRAFFIC:Hello:3:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2004);
commit; dbms_output.put_line('TRAFFIC:Hello:4:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2005);
commit; dbms_output.put_line('TRAFFIC:Hello:5:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2006);
commit; dbms_output.put_line('TRAFFIC:Hello:6:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2007);
commit; dbms_output.put_line('TRAFFIC:Hello:7:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2008);
commit; dbms_output.put_line('TRAFFIC:Hello:8:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2009);
commit; dbms_output.put_line('TRAFFIC:Hello:9:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2010);
commit; dbms_output.put_line('TRAFFIC:Hello:10:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2011);
commit; dbms_output.put_line('TRAFFIC:Hello:11:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2012);
commit; dbms_output.put_line('TRAFFIC:Hello:12:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2013);
commit; dbms_output.put_line('TRAFFIC:Hello:13:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2014);
commit; dbms_output.put_line('TRAFFIC:Hello:14:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2015);
commit; dbms_output.put_line('TRAFFIC:Hello:15:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2016);
commit; dbms_output.put_line('TRAFFIC:Hello:16:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2017);
commit; dbms_output.put_line('TRAFFIC:Hello:17:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2018);
commit; dbms_output.put_line('TRAFFIC:Hello:18:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2019);
commit; dbms_output.put_line('TRAFFIC:Hello:19:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2020);
commit; dbms_output.put_line('TRAFFIC:Hello:20:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2021);
commit; dbms_output.put_line('TRAFFIC:Hello:21:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2022);
commit; dbms_output.put_line('TRAFFIC:Hello:22:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2023);
commit; dbms_output.put_line('TRAFFIC:Hello:23:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2024);
commit; dbms_output.put_line('TRAFFIC:Hello:24:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2025);
commit; dbms_output.put_line('TRAFFIC:Hello:25:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2026);
commit; dbms_output.put_line('TRAFFIC:Hello:26:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2027);
commit; dbms_output.put_line('TRAFFIC:Hello:27:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2028);
commit; dbms_output.put_line('TRAFFIC:Hello:28:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2029);
commit; dbms_output.put_line('TRAFFIC:Hello:29:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2030);
commit; dbms_output.put_line('TRAFFIC:Hello:30:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2031);
commit; dbms_output.put_line('TRAFFIC:Hello:31:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2032);
commit; dbms_output.put_line('TRAFFIC:Hello:32:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2033);
commit; dbms_output.put_line('TRAFFIC:Hello:33:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2034);
commit; dbms_output.put_line('TRAFFIC:Hello:34:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2035);
commit; dbms_output.put_line('TRAFFIC:Hello:35:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2036);
commit; dbms_output.put_line('TRAFFIC:Hello:36:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2037);
commit; dbms_output.put_line('TRAFFIC:Hello:37:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2038);
commit; dbms_output.put_line('TRAFFIC:Hello:38:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2039);
commit; dbms_output.put_line('TRAFFIC:Hello:39:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2040);
commit; dbms_output.put_line('TRAFFIC:Hello:40:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2041);
commit; dbms_output.put_line('TRAFFIC:Hello:41:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2042);
commit; dbms_output.put_line('TRAFFIC:Hello:42:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2043);
commit; dbms_output.put_line('TRAFFIC:Hello:43:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2044);
commit; dbms_output.put_line('TRAFFIC:Hello:44:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2045);
commit; dbms_output.put_line('TRAFFIC:Hello:45:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2046);
commit; dbms_output.put_line('TRAFFIC:Hello:46:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2047);
commit; dbms_output.put_line('TRAFFIC:Hello:47:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2048);
commit; dbms_output.put_line('TRAFFIC:Hello:48:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2049);
commit; dbms_output.put_line('TRAFFIC:Hello:49:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2050);
commit; dbms_output.put_line('TRAFFIC:Hello:50:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2051);
commit; dbms_output.put_line('TRAFFIC:Hello:51:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2052);
commit; dbms_output.put_line('TRAFFIC:Hello:52:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2053);
commit; dbms_output.put_line('TRAFFIC:Hello:53:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2054);
commit; dbms_output.put_line('TRAFFIC:Hello:54:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2055);
commit; dbms_output.put_line('TRAFFIC:Hello:55:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2056);
commit; dbms_output.put_line('TRAFFIC:Hello:56:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2057);
commit; dbms_output.put_line('TRAFFIC:Hello:57:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2058);
commit; dbms_output.put_line('TRAFFIC:Hello:58:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2059);
commit; dbms_output.put_line('TRAFFIC:Hello:59:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2060);
commit; dbms_output.put_line('TRAFFIC:Hello:60:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2061);
commit; dbms_output.put_line('TRAFFIC:Hello:61:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2062);
commit; dbms_output.put_line('TRAFFIC:Hello:62:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2063);
commit; dbms_output.put_line('TRAFFIC:Hello:63:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2064);
commit; dbms_output.put_line('TRAFFIC:Hello:64:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2065);
commit; dbms_output.put_line('TRAFFIC:Hello:65:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2066);
commit; dbms_output.put_line('TRAFFIC:Hello:66:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2067);
commit; dbms_output.put_line('TRAFFIC:Hello:67:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2068);
commit; dbms_output.put_line('TRAFFIC:Hello:68:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2069);
commit; dbms_output.put_line('TRAFFIC:Hello:69:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2070);
commit; dbms_output.put_line('TRAFFIC:Hello:70:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2071);
commit; dbms_output.put_line('TRAFFIC:Hello:71:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2072);
commit; dbms_output.put_line('TRAFFIC:Hello:72:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2073);
commit; dbms_output.put_line('TRAFFIC:Hello:73:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2074);
commit; dbms_output.put_line('TRAFFIC:Hello:74:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2075);
commit; dbms_output.put_line('TRAFFIC:Hello:75:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2076);
commit; dbms_output.put_line('TRAFFIC:Hello:76:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2077);
commit; dbms_output.put_line('TRAFFIC:Hello:77:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2078);
commit; dbms_output.put_line('TRAFFIC:Hello:78:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/
begin e12_app.request('Hello',2079);
commit; dbms_output.put_line('TRAFFIC:Hello:79:'||to_char(systimestamp,'HH24:MI:SS.FF')); dbms_session.sleep(.05); end;
/

```

### World-complete.log.sql

```sql
update e12_app.callers set api=2,maintenance=0 where component='World';
insert into e12_app.migrations values('World','complete');
commit;
begin e12_app.request('World',2500);
commit; end;
/
```

### assertions.log.sql

```sql
declare n number; begin
select count(*) into n from e12_app.callers where api=2 and maintenance=0; if n<>2 then raise_application_error(-20206,'routes incomplete'); end if;
select count(*) into n from e12_app.history; if n<>163 then raise_application_error(-20207,'history lost'); end if;
select count(*) into n from e12_app.history h full outer join e12_app.details d on h.id=d.id where h.id is null or d.id is null or h.message<>case when d.template='literal' then d.person else 'Hello '||d.person end; if n<>0 then raise_application_error(-20208,'representation mismatch'); end if;
select count(*) into n from e12_app.settings where k='language' and v='en'; if n<>1 then raise_application_error(-20209,'configuration lost'); end if;
if e12_app.bridge.read_message(0)<>'retained greeting' then raise_application_error(-20210,'baseline lost'); end if;
dbms_output.put_line('COMPONENT_WINDOWS_PRESERVATION_PASS'); end;
/

```

### Interruption SQL

For Hello, the child executes the statements below, then SQLPlus `exit failure rollback`; World uses the same sequence with World substituted. These changes must remain absent after termination. No committed user data is deleted.

```sql
update e12_app.callers set api=2 where component='Hello';
insert into e12_app.migrations values('Hello','partial');
```

## 3. Execute both windows — slides 6–8

The driver performs the stages explained above against a fresh isolated schema. It preserves the run for inspection; it does not deploy to the retained application or clean unrelated schemas. This invocation takes approximately ten seconds on the prepared host.

```bash
python3 tests/foundation_windows.py integration
```

Expected final output begins `PASS real Oracle separate windows and interrupted component recovery` followed by the actual run directory. Intermediate SQL is retained there. An unexpected Oracle or transport failure raises a nonzero exception; preserve the run, correct the diagnosed issue and repeat with a fresh schema. The expected child failure alone does not establish recovery.

## 4. Inspect actual outputs — slides 7–12

The VS Code command opens the delivered evidence directory (requires code on PATH). Inspect the newly printed run directory, the two traffic logs, two recovery logs, assertions.log and receipt.json. Traffic logs contain attributable timestamps and calls 0–79; recovery logs contain RECOVERY_PASS and final assertions contain COMPONENT_WINDOWS_PRESERVATION_PASS. Confirm both maintenance rejection checks succeeded, and the history/configuration checks did not raise an error. This fulfills the bounded PBI-050 fixture journey, not arbitrary-load availability.

```bash
code progress/E.14/tests
```

### Visible greeting values from the developer's live fixture

[Actual post-recovery read](tests/run_18259/visible-greetings.log) shows the retained row `0: retained greeting`; legacy World row `1000: Hello World` has `template=literal, person=Hello World`; migrated Hello rows `1500` and `2000` contain `Hello Hello` with `template=greeting, person=Hello`; migrated World row `2500: Hello World` has `template=greeting, person=World`. These are actual database values, not injected expected results. The [read-only SQL](tests/run_18259/visible-greetings.log.sql) identifies the exact inspected rows. This saved live example is distinct from a newly generated run directory.

## 5. Assess the architecture — slides 13–18

Open the source-linked assessment and follow each earlier sprint test record. It separates validated experiments from untested production behavior and proposes a dependency-ordered Construction sequence. Review the credential-source exception, clean-host reproduction, real caller fencing and native release qualification before a separate Lifecycle Architecture decision. This fulfills PBI-080's recommendation requirement without deciding the milestone.

```bash
code progress/E.14/architecture_assessment.md
```

[Manual](user_manual.md) owns prerequisites and recovery; [handover](sprint_E.14_handover.md) owns actual live observations; [presentation](sprint_E.14_increment_demo.pptx) follows the slide map above.

## Existing production work and lifecycle records

The [production follow-up inventory](production_follow_up.md) enumerates every existing Proposed item relevant to the proposed sequence, preserving literal root statuses and linking each definition. The proposed priority groups do not reorder BACKLOG or assign a sprint. It also identifies prior E.10/E.13 backlog-versus-plan discrepancies. Review those sources separately from test behavior before the Product Owner's Lifecycle Architecture decision. No new backlog item was registered during E.14.

## Current slide map

1 cover; 2 agenda; 3 scope section header; 4 architecture; 5 journey section header; 6 actual invocation; 7 Hello window; 8 World window; 9 recovery section header; 10 window verification; 11 regression interruption/recovery; 12 evidence limits; 13 Construction section header; 14 proposed sequence; 15 existing production backlog; 16 separate architecture decision; 17 assigned outcomes; 18 Q&A. The [documentation delivery record](sprint_E.14_documentation.md) and [test record](sprint_E.14_tests.md) support this entry point.
