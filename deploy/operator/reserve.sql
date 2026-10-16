whenever oserror exit failure rollback
whenever sqlerror exit failure rollback
set define on verify off serveroutput on
begin
  dbms_output.put_line('Ownership generation: '||E1_CTRL.e1_ownership.acquire('&1','&2','&3'));
end;
/
