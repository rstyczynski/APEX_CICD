whenever oserror exit failure rollback
whenever sqlerror exit failure rollback
set define on verify off serveroutput on
declare f apex_t_export_files;
begin
  f:=apex_export.get_application(p_application_id=>to_number('&1'),p_type=>'CHECKSUM-SH256',p_with_date=>false,p_with_original_ids=>true,p_with_supporting_objects=>'N',p_with_audit_info=>null);
  for i in 1..f.count loop dbms_output.put_line(dbms_lob.substr(f(i).contents,32767,1)); end loop;
end;
/
