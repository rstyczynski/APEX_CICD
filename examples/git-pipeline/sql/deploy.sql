set echo off verify off define on
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
connect -name e3-target
begin
  if user <> 'E3_TARGET' then raise_application_error(-20931,'Unexpected target'); end if;
end;
/
define DEFAULTS_FILE = '&2'
project deploy -file &1
exit success
