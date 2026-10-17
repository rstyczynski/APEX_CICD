whenever oserror exit failure rollback
whenever sqlerror exit failure rollback
set define on verify off serveroutput on
@@../checks/initial_target.sql
begin E1_CTRL.e1_release.begin_initial(to_number('&1'),'&2','&3','&4'); end;
/
