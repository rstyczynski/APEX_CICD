-- Run only after the shell toolchain and fixture identity checks.
-- &1: private native connection alias for this independent author fixture.
set echo off verify off define on
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
connect -name &1
select user, sys_context('USERENV','SERVICE_NAME') service_name from dual;
project export -list
project export
exit success
