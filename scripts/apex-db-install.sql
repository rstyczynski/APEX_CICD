whenever oserror exit failure rollback
whenever sqlerror exit failure rollback
alter session set container=FREEPDB1;
@apexins.sql SYSAUX SYSAUX TEMP /i/
exit
