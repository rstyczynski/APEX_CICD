set echo off verify off define off
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
connect -name lab-dev-c
project export -list
project export
exit success
