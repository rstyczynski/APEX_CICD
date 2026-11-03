set echo off verify off define on
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
connect -name e3-target
-- Read-only behavior checks precede publication.
declare n number;
begin
  if user <> '&1' then raise_application_error(-20931,'Unexpected target'); end if;
  lab_runtime.assert_ready;
  select count(*) into n from apex_application_page_regions
   where application_id=&3 and page_id=1 and region_name='Hello World - Git pipeline';
  if n <> 1 then raise_application_error(-20932,'Expected Home heading missing'); end if;
  apex_util.set_security_group_id(apex_util.find_security_group_id('&2'));
  -- Native APEX executes the application's Initialization PL/SQL Code.
  apex_session.create_session(p_app_id=>&3,p_page_id=>1,p_username=>'VERIFIER');
  apex_session.delete_session;
end;
/
-- APEX availability is inherited from the E.2 native approach.
begin
  apex_util.set_security_group_id(apex_util.find_security_group_id('&1'));
  apex_application_admin.set_application_status(
    p_application_id => &3, p_application_status => apex_application_admin.c_app_available);
  commit;
end;
/
prompt PASS native readiness, heading and APEX publication
exit success
