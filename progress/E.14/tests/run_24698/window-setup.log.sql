alter table e12_app.callers add(maintenance number default 0);
create table e12_app.migrations(component varchar2(20),phase varchar2(20));
create or replace procedure e12_app.request(c varchar2,i number) is m number; begin
select maintenance into m from e12_app.callers where component=c;
if m=999 then raise_application_error(-20201,'component maintenance'); end if;
if c='Hello' then e12_app.hello(i); elsif c='World' then e12_app.world(i); else raise_application_error(-20202,'unknown component'); end if;
end;
/
