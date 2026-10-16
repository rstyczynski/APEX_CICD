whenever oserror exit failure rollback
whenever sqlerror exit failure rollback
set define on verify off serveroutput on
begin
  E1_CTRL.e1_ownership.release_task('&1',to_number('&2'));
  dbms_output.put_line('Owned task released.');
end;
/
