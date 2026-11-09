-- Reproduce the accepted original CHECK text/order in new E4 fixtures only.
-- Input: native SXML already retained in accepted Git source 1fb3bfceea.
-- SQLcl formats emitted DDL, but native snapshot preserves original condition text.
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
set define off
declare
  n number;
begin
  if user <> 'E1_DEV_C' or sys_context('USERENV','CON_NAME') not in ('E4A','E4B','E4C','E4I') then
    raise_application_error(-20942,'Expected E4 author/integration fixture'); end if;
  select count(*) into n from user_constraints where table_name='HELLO_CONFIG' and constraint_type='C' and search_condition_vc not like '"%" IS NOT NULL';
  if n <> 1 then raise_application_error(-20943,'Unexpected check count: hello_config'); end if;
  for c in (select constraint_name from user_constraints where table_name='HELLO_CONFIG' and constraint_type='C' and search_condition_vc not like '"%" IS NOT NULL') loop
    execute immediate 'alter table hello_config drop constraint '||dbms_assert.enquote_name(c.constraint_name);
  end loop;
  execute immediate q'~alter table hello_config add check (config_id=1) enable~';
  select count(*) into n from user_constraints where table_name='HELLO_ENTRIES' and constraint_type='C' and search_condition_vc not like '"%" IS NOT NULL';
  if n <> 3 then raise_application_error(-20943,'Unexpected check count: hello_entries'); end if;
  for c in (select constraint_name from user_constraints where table_name='HELLO_ENTRIES' and constraint_type='C' and search_condition_vc not like '"%" IS NOT NULL') loop
    execute immediate 'alter table hello_entries drop constraint '||dbms_assert.enquote_name(c.constraint_name);
  end loop;
  execute immediate q'~alter table hello_entries add constraint HELLO_TEXT_NONBLANK check (regexp_like(entry_text,'[^[:space:]]')) enable~';
  execute immediate q'~alter table hello_entries add check (active in ('Y','N')) enable~';
  execute immediate q'~alter table hello_entries add constraint HELLO_TEXT_VALID check (length(trim(entry_text)) between 1 and 100) enable~';
  select count(*) into n from user_constraints where table_name='LAB_COMPONENTS' and constraint_type='C' and search_condition_vc not like '"%" IS NOT NULL';
  if n <> 2 then raise_application_error(-20943,'Unexpected check count: lab_components'); end if;
  for c in (select constraint_name from user_constraints where table_name='LAB_COMPONENTS' and constraint_type='C' and search_condition_vc not like '"%" IS NOT NULL') loop
    execute immediate 'alter table lab_components drop constraint '||dbms_assert.enquote_name(c.constraint_name);
  end loop;
  execute immediate q'~alter table lab_components add check (installed in (0,1)) enable~';
  execute immediate q'~alter table lab_components add constraint LAB_COMPONENT_PRESENCE check ((installed=0 and version is null) or (installed=1 and version is not null)) enable~';
  select count(*) into n from user_constraints where table_name='LAB_STATE' and constraint_type='C' and search_condition_vc not like '"%" IS NOT NULL';
  if n <> 1 then raise_application_error(-20943,'Unexpected check count: lab_state'); end if;
  for c in (select constraint_name from user_constraints where table_name='LAB_STATE' and constraint_type='C' and search_condition_vc not like '"%" IS NOT NULL') loop
    execute immediate 'alter table lab_state drop constraint '||dbms_assert.enquote_name(c.constraint_name);
  end loop;
  execute immediate q'~alter table lab_state add check (state in ('ready','maintenance','failed')) enable~';
  select count(*) into n from user_constraints where table_name='WORLD_CONFIG' and constraint_type='C' and search_condition_vc not like '"%" IS NOT NULL';
  if n <> 1 then raise_application_error(-20943,'Unexpected check count: world_config'); end if;
  for c in (select constraint_name from user_constraints where table_name='WORLD_CONFIG' and constraint_type='C' and search_condition_vc not like '"%" IS NOT NULL') loop
    execute immediate 'alter table world_config drop constraint '||dbms_assert.enquote_name(c.constraint_name);
  end loop;
  execute immediate q'~alter table world_config add check (config_id=1) enable~';
  select count(*) into n from user_constraints where table_name='WORLD_ENTRIES' and constraint_type='C' and search_condition_vc not like '"%" IS NOT NULL';
  if n <> 2 then raise_application_error(-20943,'Unexpected check count: world_entries'); end if;
  for c in (select constraint_name from user_constraints where table_name='WORLD_ENTRIES' and constraint_type='C' and search_condition_vc not like '"%" IS NOT NULL') loop
    execute immediate 'alter table world_entries drop constraint '||dbms_assert.enquote_name(c.constraint_name);
  end loop;
  execute immediate q'~alter table world_entries add check (active in ('Y','N')) enable~';
  execute immediate q'~alter table world_entries add constraint WORLD_TEXT_VALID check (length(trim(entry_text)) between 1 and 100) enable~';
end;
/
