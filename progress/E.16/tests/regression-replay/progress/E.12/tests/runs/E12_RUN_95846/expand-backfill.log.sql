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
