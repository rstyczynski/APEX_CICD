whenever oserror exit failure rollback
whenever sqlerror exit failure rollback
set define on verify off serveroutput on
declare n number;
begin
  if user<>'E1_DEV_C' then raise_application_error(-20603,'Release verification target not registered'); end if;
  select count(*) into n from user_errors;
  if n<>0 then raise_application_error(-20604,'Compile errors block release'); end if;
  select count(*) into n from lab_components where installed=1 and ((component in ('Foundation','World') and version='1.0.0') or (component='Hello' and version='1.0.1'));
  if n<>3 then raise_application_error(-20605,'Unsupported complete component triple'); end if;
  select count(*) into n from lab_state where state_key in ('Foundation','Hello','World') and state='ready';
  if n<>3 then raise_application_error(-20606,'Component dependency not ready'); end if;
  select count(*) into n from databasechangelog;
  if n<>5 then raise_application_error(-20607,'Expected five immutable migrations'); end if;
  select count(*) into n from databasechangelog where author='apex-lab' and id in ('001-foundation','002-foundation-runtime','003-hello','004-world','005-hello-1.0.1');
  if n<>5 then raise_application_error(-20624,'Unknown migration identities'); end if;
  select count(*) into n from apex_applications where application_id=810003 and version='1.0.1';
  if n<>1 then raise_application_error(-20625,'APEX application version differs from release'); end if;
  select count(*) into n from apex_release where version_no='24.2.0';
  if n<>1 then raise_application_error(-20626,'Unsupported APEX version'); end if;
  select count(*) into n from apex_application_pages where application_id=810003 and page_id in (0,1,10,20,100,101,110,111,200,201,210,211,9999);
  if n<>13 then raise_application_error(-20608,'Required pages missing'); end if;
  dbms_output.put_line('PASS patch release integrity: Foundation/World 1.0.0, Hello 1.0.1, migrations and pages.');
end;
/
