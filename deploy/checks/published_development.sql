whenever oserror exit failure rollback
whenever sqlerror exit failure rollback
set serveroutput on
@@complete_assembly.sql
declare n number;
begin
  select count(*) into n from lab_state where state_key='Application' and state='ready';
  if n<>1 then raise_application_error(-20425,'Development runtime is not ready'); end if;
  select count(*) into n from apex_applications where application_id=810003 and upper(availability_status)='AVAILABLE';
  if n<>1 then raise_application_error(-20426,'Development application is not available'); end if;
  dbms_output.put_line('PASS published development: native availability and application ready state.');
end;
/
