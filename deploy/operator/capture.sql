whenever oserror exit failure rollback
whenever sqlerror exit failure rollback
set define on verify off serveroutput on
declare n number;
begin
  apex_util.set_workspace('&6');
  E1_CTRL.e1_ownership.assert_owned('&2','&3',to_number('&4'));
  select count(*) into n from apex_applications where application_id=to_number('&1') and workspace='&6';
  if n<>1 then raise_application_error(-20210,'Application/workspace mapping does not match capture'); end if;
  dbms_output.put_line('Task ownership and capture application verified.');
end;
/
apex export -applicationid &1 -split -skipExportDate -expOriginalIds -expSupportingObjects N -dir &5
