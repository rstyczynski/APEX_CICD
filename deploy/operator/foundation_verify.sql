whenever oserror exit failure rollback
whenever sqlerror exit failure rollback
set serveroutput on
declare n number;
begin
  select count(*) into n from lab_components where component='Foundation' and installed=1 and version='1.0.0';
  if n<>1 then raise_application_error(-20201,'Foundation version check failed'); end if;
  select count(*) into n from lab_components where component in ('Hello','World') and installed=0 and version is null;
  if n<>2 then raise_application_error(-20202,'Expected Hello/World not installed'); end if;
  select count(*) into n from lab_state where state_key='Application' and state='maintenance';
  if n<>1 then raise_application_error(-20203,'Incomplete application is not blocked'); end if;
  dbms_output.put_line('Foundation verified; Hello/World absent; application remains in maintenance.');
end;
/
