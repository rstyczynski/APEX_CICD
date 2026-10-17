whenever oserror exit failure rollback
whenever sqlerror exit failure rollback
set serveroutput on
@@identity.sql E1_DEV_C E1_DEV_C
@@assert_ownership.sql Foundation compose-initial 5
@@assert_ownership.sql Hello compose-initial 5
@@assert_ownership.sql World compose-initial 5
@@../checks/complete_assembly.sql
declare n number;
begin
  select count(*) into n from greeting_history where greeting_text='Hello World' and actor='VERIFIER';
  if n=0 then raise_application_error(-20424,'Browser verification snapshot required before development publication'); end if;
  apex_util.set_workspace('E1_DEV_C');
  apex_application_admin.set_application_status(
    p_application_id=>810003,
    p_application_status=>apex_application_admin.c_app_available);
  update lab_state set state='ready',reason='Development assembly: verified greeting and history' where state_key='Application';
  commit;
  dbms_output.put_line('PUBLISHED DEVELOPMENT: application 810003. Qualification and TEST promotion remain separate gates.');
end;
/
