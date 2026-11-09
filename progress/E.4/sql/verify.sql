-- &1: author connection; &2: reviewed comparison branch for this Git state.
set echo off verify off define on
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
connect -name &1
project verify -cbn &2 -verbose
exit success
