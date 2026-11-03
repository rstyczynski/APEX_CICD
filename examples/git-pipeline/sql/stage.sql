set echo off verify off define off
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
connect -name lab-dev-c
project stage -branch-name e3-base
exit success
