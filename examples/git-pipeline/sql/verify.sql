set echo off verify off define off
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
connect -name lab-dev-c
project verify -cbn e3-base -verbose
exit success
