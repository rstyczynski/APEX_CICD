-- &1: connection; &2: expected schema; &3: workspace; &4: application.
-- Invoke only after acceptance checks and full business-field comparison pass.
set echo off verify off define on
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
connect -name &1
begin
  if user <> '&2' then raise_application_error(-20931,'Unexpected target'); end if;
  apex_util.set_workspace(p_workspace=>'&3');
  apex_application_admin.set_application_status(
    p_application_id=>&4,
    p_application_status=>apex_application_admin.c_app_available);
  commit;
end;
/
exit success
