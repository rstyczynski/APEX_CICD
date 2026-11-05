set echo off verify off define on
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
project release -version &1
exit success
