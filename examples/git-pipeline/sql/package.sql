set echo off verify off define on
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
project gen-artifact -name e3 -version &1 -format zip
exit success
