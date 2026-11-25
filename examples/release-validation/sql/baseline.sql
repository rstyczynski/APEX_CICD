create table e7_app.greetings(id number primary key, message varchar2(100) not null);
create table e7_app.release_reference(code varchar2(20) primary key, value varchar2(40));
insert into e7_app.release_reference values('LANGUAGE','en');
create table e7_app.migrations(version varchar2(20) primary key);
insert into e7_app.migrations values('1.0.0');
create or replace package e7_app.greeting_api as function render(p_text varchar2) return varchar2; end;
/
create or replace package body e7_app.greeting_api as function render(p_text varchar2) return varchar2 is begin return 'Hello '||trim(p_text); end; end;
/
grant execute on e7_app.greeting_api to e7_consumer;
commit;
