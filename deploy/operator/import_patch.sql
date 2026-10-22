whenever oserror exit failure rollback
whenever sqlerror exit failure rollback
set define on verify off serveroutput on
-- Run only after identity, ownership, source and initial-target checks.
declare n number; files apex_t_export_files; captured_offset varchar2(100);
begin
  if user<>'&3' then raise_application_error(-20212,'Import target schema mismatch'); end if;
  select count(*) into n from apex_workspace_schemas where workspace_name='&1' and schema='&3';
  if n<>1 then raise_application_error(-20213,'Import workspace mapping mismatch'); end if;
  select count(*) into n from apex_applications where application_id=to_number('&2') and workspace='&1';
  if n<>1 then raise_application_error(-20645,'Patch import requires the existing baseline application'); end if;
  apex_application_install.set_workspace('&1');
  apex_application_install.set_application_id(to_number('&2'));
  apex_application_install.set_schema('&3');
  apex_application_install.set_application_alias('&4');
  -- Observe the owned installed application through the public export API.
  -- Replacement must retain its offset, not generate a new component identity.
  commit; -- APEX export owns a read-only transaction.
  files := apex_export.get_application(p_application_id=>to_number('&2'),
    p_type=>'APPLICATION_SOURCE',p_with_date=>false,p_with_original_ids=>true,
    p_with_supporting_objects=>'N',p_with_audit_info=>null);
  if files.count<>1 then raise_application_error(-20820,'Single installed application export required for replacement identity'); end if;
  captured_offset:=regexp_substr(files(1).contents,'p_default_id_offset=>[[:space:]]*([0-9]+)',1,1,'c',1);
  if captured_offset is null or not regexp_like(captured_offset,'^[0-9]{1,20}$') then
    raise_application_error(-20821,'Installed application offset missing or invalid');
  end if;
  commit; -- End export transaction before native import DML.
  apex_application_install.set_offset(to_number(captured_offset));
  dbms_output.put_line('REUSED_APEX_OFFSET='||captured_offset);
end;
/
@"&5/install.sql"
