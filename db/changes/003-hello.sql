create table hello_entries (
  entry_id number generated always as identity primary key,
  entry_text varchar2(100 char) not null,
  active char(1) default 'Y' not null check (active in ('Y','N')),
  constraint hello_text_valid check (length(trim(entry_text)) between 1 and 100)
)
/
create table hello_config (
  config_id number primary key check (config_id=1),
  prefix varchar2(30 char),
  default_entry_id number references hello_entries(entry_id)
)
/
insert into hello_config(config_id) values (1)
/
create or replace trigger hello_entries_guard
before insert or update on hello_entries for each row
declare n number;
begin
  lab_runtime.assert_ready;
  :new.entry_text:=trim(:new.entry_text);
  if :new.active='N' then
    select count(*) into n from hello_config where default_entry_id=:new.entry_id;
    if n>0 then raise_application_error(-20310,'Choose another active Hello default before deactivation'); end if;
  end if;
end;
/
create or replace trigger hello_entries_no_delete
before delete on hello_entries
begin raise_application_error(-20311,'Deactivate Hello entries instead of deleting'); end;
/
create or replace trigger hello_config_guard
before insert or update on hello_config for each row
declare n number;
begin
  lab_runtime.assert_ready;
  select count(*) into n from hello_entries where entry_id=:new.default_entry_id and active='Y';
  if n<>1 then raise_application_error(-20312,'Hello default must be an active Hello entry'); end if;
end;
/
create or replace trigger hello_config_no_delete
before delete on hello_config
begin raise_application_error(-20313,'Hello configuration cannot be deleted'); end;
/
update lab_components set installed=1,version='1.0.0' where component='Hello'
/
update lab_state set state='ready',reason='Hello installed; complete application still blocked' where state_key='Hello'
/
