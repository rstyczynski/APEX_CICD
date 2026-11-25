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
exception when others then null; raise;
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
