whenever oserror exit failure rollback
whenever sqlerror exit failure rollback
set define on verify off serveroutput on
begin E1_CTRL.e1_release.assert_attempt(to_number('&1'),'&2'); end;
/
