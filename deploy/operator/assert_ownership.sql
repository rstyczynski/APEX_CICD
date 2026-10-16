whenever oserror exit failure rollback
whenever sqlerror exit failure rollback
set define on verify off serveroutput on
begin
  E1_CTRL.e1_ownership.assert_owned('&1','&2',to_number('&3'));
  dbms_output.put_line('Task ownership verified for connected schema.');
end;
/
