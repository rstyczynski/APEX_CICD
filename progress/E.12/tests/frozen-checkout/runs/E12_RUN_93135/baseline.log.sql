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
