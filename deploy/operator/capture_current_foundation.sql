whenever oserror exit failure rollback
whenever sqlerror exit failure rollback
set define on verify off serveroutput on
variable capture_generation number
begin
  if user<>'E1_DEV_A' then raise_application_error(-20210,'Foundation capture requires E1_DEV_A'); end if;
  apex_util.set_workspace('E1_DEV_A');
  if not regexp_like('&3','^[a-zA-Z0-9_-]{1,80}$') then raise_application_error(-20211,'Invalid capture task'); end if;
  :capture_generation:=E1_CTRL.e1_ownership.acquire('Foundation','&3','&1');
  E1_CTRL.e1_ownership.assert_owned('Foundation','&3',:capture_generation);
end;
/
apex export -applicationid 810001 -split -skipExportDate -expOriginalIds -expSupportingObjects N -dir &2
begin
  E1_CTRL.e1_ownership.release_task('&3',:capture_generation);
  dbms_output.put_line('Foundation capture task released.');
end;
/
