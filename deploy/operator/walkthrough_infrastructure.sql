-- Infrastructure inventory only: no application or database writes.
whenever oserror exit failure
whenever sqlerror exit failure
alter session set container=FREEPDB1;
set serveroutput on
declare n number;
begin
 select count(*) into n from dba_registry where comp_id='APEX';
 if n=0 then dbms_output.put_line('EXISTING DATABASE: APEX is not installed.');
 else
  for r in (select version,status from dba_registry where comp_id='APEX') loop
   dbms_output.put_line('EXISTING APEX: version='||r.version||' status='||r.status);
  end loop;
 end if;
 dbms_output.put_line('PRECHECK_APEX_INFO_COMPLETE');
end;
/
exit success
