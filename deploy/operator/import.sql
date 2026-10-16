whenever oserror exit failure rollback
whenever sqlerror exit failure rollback
set define on verify off serveroutput on
-- Run only after identity, ownership, source and initial-target checks.
declare n number;
begin
  if user<>'&3' then raise_application_error(-20212,'Import target schema mismatch'); end if;
  select count(*) into n from apex_workspace_schemas where workspace_name='&1' and schema='&3';
  if n<>1 then raise_application_error(-20213,'Import workspace mapping mismatch'); end if;
  select count(*) into n from apex_applications where application_id=to_number('&2');
  if n<>0 then raise_application_error(-20214,'Initial import refuses an existing application'); end if;
  apex_application_install.set_workspace('&1');
  apex_application_install.set_application_id(to_number('&2'));
  apex_application_install.set_schema('&3');
  apex_application_install.set_application_alias('&4');
  apex_application_install.generate_offset;
end;
/
@&5/install.sql
