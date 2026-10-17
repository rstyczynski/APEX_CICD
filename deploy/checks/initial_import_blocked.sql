whenever oserror exit failure rollback
whenever sqlerror exit failure rollback
set define on verify off serveroutput on
declare n number;
begin
 select count(*) into n from apex_applications where application_id=to_number('&1') and upper(availability_status)='UNAVAILABLE';
 if n<>1 then raise_application_error(-20622,'Imported application must remain natively unavailable'); end if;
 select count(*) into n from lab_state where state_key='Application' and state='maintenance';
 if n<>1 then raise_application_error(-20623,'Initial import reset the maintenance gate'); end if;
 dbms_output.put_line('PASS imported source is unavailable and root remains in maintenance.');
end;
/
