whenever oserror exit failure rollback
whenever sqlerror exit failure rollback
set pagesize 100 linesize 200
alter session set container=FREEPDB1;
select sys_context('USERENV','CON_NAME') as container_name from dual;
select comp_id, version, status from dba_registry where comp_id = 'APEX';
select version_no from apex_release;
select username, account_status from dba_users
where username in ('APEX_PUBLIC_USER','ORDS_PUBLIC_USER','APEX_REST_PUBLIC_USER','APEX_LISTENER');
select count(*) as invalid_apex_objects from dba_objects
where owner = 'APEX_240200' and status = 'INVALID';
declare
  l_count number;
begin
  select count(*) into l_count from dba_registry
  where comp_id = 'APEX' and status = 'VALID' and version like '24.2%';
  if l_count <> 1 then raise_application_error(-20001, 'APEX 24.2 is not VALID'); end if;
  select count(*) into l_count from dba_objects
  where owner = 'APEX_240200' and status = 'INVALID';
  if l_count <> 0 then raise_application_error(-20002, 'Invalid APEX objects exist'); end if;
end;
/
exit
