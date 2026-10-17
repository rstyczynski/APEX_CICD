whenever oserror exit failure rollback
whenever sqlerror exit failure rollback
set serveroutput on
@@identity.sql E1_DEV_C E1_DEV_C
@@assert_ownership.sql Foundation compose-initial 5
@@assert_ownership.sql Hello compose-initial 5
@@assert_ownership.sql World compose-initial 5
@@../checks/complete_assembly.sql
begin
  apex_util.set_workspace('E1_DEV_C');
  apex_application_admin.set_application_status(
    p_application_id=>810003,
    p_application_status=>apex_application_admin.c_app_restricted_access,
    p_allowed_users_list=>apex_t_varchar2('VERIFIER'),
    p_message=>'Development verification in progress.');
  update lab_state set state='ready',reason='Development assembly: restricted browser verification' where state_key='Application';
  commit;
  dbms_output.put_line('Development runtime restricted to VERIFIER. Ordinary application accounts remain blocked.');
end;
/
