whenever oserror exit failure rollback
whenever sqlerror exit failure rollback
set define on verify off serveroutput on
define release_epoch = '&1'
define release_app = '&2'
define release_hash = '&3'
begin E1_CTRL.e1_release.assert_attempt(to_number('&release_epoch'),'&release_hash'); end;
/
@@../checks/patch_integrity.sql &release_app
-- Stage native availability while the independent external gate is still verifying.
declare n number;
begin
  select count(*) into n from greeting_history where actor='VERIFIER' and greeting_text='Hello World';
  if n<1 then raise_application_error(-20619,'Verified runtime snapshot missing'); end if;
  apex_util.set_workspace(user);
  apex_application_admin.set_application_status(to_number('&release_app'),apex_application_admin.c_app_available);
  commit;
end;
/
-- APEX_EXPORT starts a read-only transaction. It cannot follow status DML.
variable final_release_fingerprint varchar2(4000)
declare files apex_t_export_files;
begin
  apex_util.set_workspace(user);
  commit;
  files:=apex_export.get_application(p_application_id=>to_number('&release_app'),p_type=>'CHECKSUM-SH256',p_with_date=>false,p_with_original_ids=>true,p_with_supporting_objects=>'N',p_with_audit_info=>null);
  if files.count<>1 then raise_application_error(-20620,'Unexpected fingerprint result'); end if;
  :final_release_fingerprint:=rtrim(dbms_lob.substr(files(1).contents,4000,1),chr(10)||chr(13)||' ');
  commit;
end;
/
-- Open the external gate atomically with the successful receipt.
declare n number; state_before varchar2(20);
begin
  E1_CTRL.e1_release.assert_attempt(to_number('&release_epoch'),'&release_hash');
  select state into state_before from lab_state where state_key='Application' for update nowait;
  if state_before<>'ready' then raise_application_error(-20634,'Verification readiness changed before publication'); end if;
  select count(*) into n from apex_applications where application_id=to_number('&release_app') and upper(availability_status)='AVAILABLE';
  if n<>1 then raise_application_error(-20635,'Final native availability is not prepared'); end if;
  update lab_state set state='ready',reason='Hello patch verified and published' where state_key='Application';
  E1_CTRL.e1_release.publish_initial(to_number('&release_epoch'),'&release_hash',:final_release_fingerprint);
  commit;
  dbms_output.put_line('PUBLISHED HELLO PATCH: successful receipt and external ready gate committed together.');
  dbms_output.put_line(:final_release_fingerprint);
end;
/
