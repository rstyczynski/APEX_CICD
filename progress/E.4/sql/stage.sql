-- &1: author connection; &2: immutable comparison branch in this checkout.
set echo off verify off define on
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
connect -name &1
project stage -branch-name &2
exit success
