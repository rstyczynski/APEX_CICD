-- &1: connection; &2: expected schema; &3: workspace; &4: application.
-- Session context only; this script does not change application state.
set echo off verify off define on serveroutput on
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
connect -name &1
set serveroutput on
declare
  files apex_t_export_files;
  status varchar2(100);
begin
  if user <> '&2' then raise_application_error(-20931,'Unexpected target'); end if;
  apex_util.set_workspace(p_workspace=>'&3');
  select availability_status into status from apex_applications where application_id=&4;
  files := apex_export.get_application(
    p_application_id=>&4, p_type=>'CHECKSUM-SH256',
    p_with_date=>false, p_with_original_ids=>true,
    p_with_ir_public_reports=>true, p_with_ir_private_reports=>false,
    p_with_ir_notifications=>false, p_with_translations=>false,
    p_with_comments=>false, p_with_supporting_objects=>'N',
    p_with_acl_assignments=>false, p_with_audit_info=>null);
  dbms_output.put_line('E4_STATUS='||status);
  dbms_output.put_line('E4_CHECKSUM='||dbms_lob.substr(files(1).contents,32767,1));
end;
/
exit success
