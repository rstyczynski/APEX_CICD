set echo off verify off define on serveroutput off
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
connect -name e3-target
begin
  if user <> 'E3_TARGET' then raise_application_error(-20931,'Unexpected target'); end if;
end;
/
set heading off pagesize 0 feedback off linesize 32767 long 1000000 longchunksize 32767 trimspool on
spool &1
select 'greeting_history|'||json_object(*) from greeting_history order by greeting_id;
select 'hello_entries|'||json_object(*) from hello_entries order by entry_id;
select 'world_entries|'||json_object(*) from world_entries order by entry_id;
select 'hello_config|'||json_object(*) from hello_config order by config_id;
select 'world_config|'||json_object(*) from world_config order by config_id;
select 'lab_components|'||json_object(*) from lab_components order by component;
select 'lab_state|'||json_object(*) from lab_state order by state_key;
spool off
exit success
