-- Fixed E4A only. Run as SYS in E4A after APEX 24.2 installation.
-- &1 and &2 are new temporary author and ORDS-install administrator passwords.
set echo off verify off
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
alter session set container=E4A;
create tablespace E4_DATA datafile '/opt/oracle/oradata/FREE/E4A/e4_data.dbf'
  size 32m autoextend on next 16m maxsize 256m;
create user E1_DEV_C identified by "&1" default tablespace E4_DATA quota unlimited on E4_DATA;
grant create session, create table, create sequence, create procedure,
  create trigger, create view to E1_DEV_C;
create user E4_ORDS_INSTALL identified by "&2";
grant dba to E4_ORDS_INSTALL;
begin
  apex_instance_admin.add_workspace(
    p_workspace_id=>3069011249066219, p_workspace=>'E1_DEV_C',
    p_primary_schema=>'E1_DEV_C');
  commit;
end;
/
exit
