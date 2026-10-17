whenever oserror exit failure rollback
whenever sqlerror exit failure rollback
set serveroutput on
declare n number;
begin
  select count(*) into n from product_component_version where product like '%Database%' and version_full='23.26.3.0.0';
  if n<>1 then raise_application_error(-20628,'Database version differs from the pinned initial-release environment'); end if;
  select count(*) into n from apex_release where version_no='24.2.0';
  if n<>1 then raise_application_error(-20626,'APEX version differs from the release environment'); end if;
  dbms_output.put_line('PASS pinned Database 23.26.3.0.0 / APEX 24.2.0 environment.');
end;
/
