whenever oserror exit failure rollback
whenever sqlerror exit failure rollback
set serveroutput on
@@identity.sql E1_DEV_C E1_DEV_C
@@../checks/published_development.sql
-- Demo configuration only. No DELETE, DDL, history write or target recreation.
declare h number; w number;
begin
  lab_runtime.assert_ready;
  select min(entry_id) into h from hello_entries where entry_text='Hello' and active='Y';
  if h is null then insert into hello_entries(entry_text,active) values ('Hello','Y') returning entry_id into h; end if;
  select min(entry_id) into w from world_entries where entry_text='World' and active='Y';
  if w is null then insert into world_entries(entry_text,active) values ('World','Y') returning entry_id into w; end if;
  update hello_config set default_entry_id=h,prefix=null where config_id=1;
  if sql%rowcount<>1 then raise_application_error(-20703,'Missing Hello configuration'); end if;
  update world_config set default_entry_id=w,prefix=null where config_id=1;
  if sql%rowcount<>1 then raise_application_error(-20704,'Missing World configuration'); end if;
  commit;
  dbms_output.put_line('PREPARED: C defaults = Hello / World, empty prefixes. All history and other entries retained.');
exception when others then rollback; raise;
end;
/
