create table world_entries (
  entry_id number generated always as identity primary key,
  entry_text varchar2(100 char) not null,
  active char(1) default 'Y' not null check (active in ('Y','N')),
  constraint world_text_valid check (length(trim(entry_text)) between 1 and 100)
)
/
create table world_config (
  config_id number primary key check (config_id=1),
  prefix varchar2(30 char),
  default_entry_id number references world_entries(entry_id)
)
/
insert into world_config(config_id) values (1)
/
create or replace trigger world_entries_guard
before insert or update on world_entries for each row
declare n number;
begin
  lab_runtime.assert_ready;
  :new.entry_text:=trim(:new.entry_text);
  if :new.active='N' then
    select count(*) into n from world_config where default_entry_id=:new.entry_id;
    if n>0 then raise_application_error(-20320,'Choose another active World default before deactivation'); end if;
  end if;
end;
/
create or replace trigger world_entries_no_delete
before delete on world_entries
begin raise_application_error(-20321,'Deactivate World entries instead of deleting'); end;
/
create or replace trigger world_config_guard
before insert or update on world_config for each row
declare n number;
begin
  lab_runtime.assert_ready;
  select count(*) into n from world_entries where entry_id=:new.default_entry_id and active='Y';
  if n<>1 then raise_application_error(-20322,'World default must be an active World entry'); end if;
end;
/
create or replace trigger world_config_no_delete
before delete on world_config
begin raise_application_error(-20323,'World configuration cannot be deleted'); end;
/
update lab_components set installed=1,version='1.0.0' where component='World'
/
update lab_state set state='ready',reason='World installed; complete application still blocked' where state_key='World'
/
