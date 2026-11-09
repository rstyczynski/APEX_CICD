-- New E4A fixture only, as SYS. &1 is the temporary Builder password.
set echo off verify off
whenever sqlerror exit failure rollback
alter session set container=E4A;
begin
  apex_util.set_workspace(p_workspace=>'E1_DEV_C');
  apex_util.create_user(p_user_name=>'E4_DEVELOPER',p_web_password=>'&1',
    p_email_address=>'e4@example.invalid',p_default_schema=>'E1_DEV_C',
    p_developer_privs=>'ADMIN:CREATE:DATA_LOADER:EDIT:HELP:MONITOR:SQL',
    p_change_password_on_first_use=>'N');
  commit;
end;
/
-- The ORDS installer has finished; its fixture-only privileged account is removed.
drop user E4_ORDS_INSTALL;
exit
