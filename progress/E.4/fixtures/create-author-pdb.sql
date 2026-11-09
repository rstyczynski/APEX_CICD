-- One-time, fixed E.4 lab fixture, run as SYS in CDB$ROOT.
-- Creates no user data copies and does not change FREEPDB1.
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
set echo off verify off
-- &1 is a newly generated temporary fixture password, never a retained host secret.
create pluggable database E4A admin user E4_PDB_ADMIN identified by "&1"
  file_name_convert=('/opt/oracle/oradata/FREE/pdbseed/','/opt/oracle/oradata/FREE/E4A/');
alter pluggable database E4A open;
alter session set container=E4A;
alter user E4_PDB_ADMIN account lock;
set define off
@/tmp/apex/apexins.sql SYSAUX SYSAUX TEMP /i/
select version_no from apex_release;
exit
