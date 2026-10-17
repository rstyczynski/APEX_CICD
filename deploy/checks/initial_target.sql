whenever oserror exit failure rollback
whenever sqlerror exit failure rollback
set serveroutput on
declare n number;
begin
  select count(*) into n from user_tables where table_name<>'E1_PRIVATE_PROBE';
  if n<>0 then raise_application_error(-20600,'Initial release requires an empty application schema'); end if;
  select count(*) into n from user_objects where object_type in ('PACKAGE','PROCEDURE','FUNCTION','VIEW','TRIGGER');
  if n<>0 then raise_application_error(-20601,'Existing program objects block initial installation'); end if;
  select count(*) into n from user_objects o where not
    ((o.object_type='TABLE' and o.object_name='E1_PRIVATE_PROBE') or
     (o.object_type='INDEX' and o.object_name in (select index_name from user_indexes where table_name='E1_PRIVATE_PROBE')));
  if n<>0 then raise_application_error(-20627,'Unexpected existing schema objects block initial installation'); end if;
  select count(*) into n from apex_applications;
  if n<>0 then raise_application_error(-20602,'Existing application requires an explicit upgrade or adoption path'); end if;
  dbms_output.put_line('PASS empty initial target; isolation probe is retained.');
end;
/
