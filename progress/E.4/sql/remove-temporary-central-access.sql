-- Prepared host only: SYS in the existing apex-db CDB, after final validation.
-- Removes only the explicitly authorized E.4 temporary identities.
set echo off verify off serveroutput on
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
alter session set container=FREEPDB1;
begin
  apex_util.set_workspace(p_workspace=>'E3_TARGET');
  apex_util.remove_user(p_user_name=>'E4_VERIFY');
  commit;
end;
/
alter user E3_TARGET revoke connect through E4_SYNC;
drop user E4_SYNC;
select count(*) temporary_database_users from dba_users where username='E4_SYNC';
select count(*) temporary_builder_users from apex_workspace_apex_users
 where workspace_name='E3_TARGET' and user_name='E4_VERIFY';
select application_id,availability_status from apex_applications
 where application_id=810203;
exit
