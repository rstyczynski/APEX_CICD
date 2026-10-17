whenever oserror exit failure rollback
whenever sqlerror exit failure rollback
set define on verify off serveroutput on
define release_epoch = '&1'
define release_app = '&2'
define release_hash = '&3'
begin E1_CTRL.e1_release.assert_attempt(to_number('&release_epoch'),'&release_hash'); end;
/
@@../checks/patch_integrity.sql &release_app
declare n number;
begin
  apex_util.set_workspace(user);
  apex_application_admin.set_application_status(to_number('&release_app'),apex_application_admin.c_app_restricted_access,
    p_allowed_users_list=>apex_t_varchar2('VERIFIER'),p_message=>'Hello patch verification in progress.');
  update lab_state set state='ready',reason='Hello patch restricted verification' where state_key='Application';
  E1_CTRL.e1_release.verifying(to_number('&release_epoch'),'&release_hash');
  commit;
  dbms_output.put_line('VERIFICATION ENABLED: VERIFIER only; ordinary accounts blocked.');
end;
/
