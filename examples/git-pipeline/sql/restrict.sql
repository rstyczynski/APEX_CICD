set echo off verify off define on
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
connect -name e3-target
begin
  if user <> '&1' then raise_application_error(-20931,'Unexpected target'); end if;
  apex_util.set_security_group_id(apex_util.find_security_group_id('&2'));
  apex_application_admin.set_application_status(
    p_application_id => &3, p_application_status => apex_application_admin.c_app_restricted_access,
    p_allowed_users_list => apex_t_varchar2('VERIFIER'));
  commit;
end;
/
exit success
