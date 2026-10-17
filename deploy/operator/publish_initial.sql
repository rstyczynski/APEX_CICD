whenever oserror exit failure rollback
whenever sqlerror exit failure rollback
set define on verify off serveroutput on
define release_epoch = '&1'
define release_app = '&2'
define release_hash = '&3'
begin E1_CTRL.e1_release.assert_attempt(to_number('&release_epoch'),'&release_hash'); end;
/
@@../checks/release_integrity.sql &release_app
declare n number; files apex_t_export_files; fingerprint varchar2(4000);
begin
  select count(*) into n from greeting_history where actor='VERIFIER' and greeting_text='Hello World';
  if n<1 then raise_application_error(-20619,'Verified runtime snapshot missing'); end if;
  apex_util.set_workspace(user);
  apex_application_admin.set_application_status(to_number('&release_app'),apex_application_admin.c_app_available);
  files:=apex_export.get_application(p_application_id=>to_number('&release_app'),p_type=>'CHECKSUM-SH256',p_with_date=>false,p_with_original_ids=>true,p_with_supporting_objects=>'N',p_with_audit_info=>null);
  if files.count<>1 then raise_application_error(-20620,'Unexpected fingerprint result'); end if;
  fingerprint:=dbms_lob.substr(files(1).contents,4000,1);
  update lab_state set state='ready',reason='Initial release verified and published' where state_key='Application';
  E1_CTRL.e1_release.publish_initial(to_number('&release_epoch'),'&release_hash',fingerprint);
  commit;
  dbms_output.put_line('PUBLISHED INITIAL RELEASE; target receipt/fingerprint/native availability committed.');
  dbms_output.put_line(fingerprint);
end;
/
