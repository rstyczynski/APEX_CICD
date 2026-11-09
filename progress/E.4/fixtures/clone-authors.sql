-- Clone only the new, synthetic E4A fixture. No retained PDB or user data is copied.
whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
set echo on
alter pluggable database E4A close immediate;
alter pluggable database E4A open read only;
create pluggable database E4B from E4A
 file_name_convert=('/opt/oracle/oradata/FREE/E4A/','/opt/oracle/oradata/FREE/E4B/');
create pluggable database E4C from E4A
 file_name_convert=('/opt/oracle/oradata/FREE/E4A/','/opt/oracle/oradata/FREE/E4C/');
create pluggable database E4I from E4A
 file_name_convert=('/opt/oracle/oradata/FREE/E4A/','/opt/oracle/oradata/FREE/E4I/');
alter pluggable database E4A close immediate;
alter pluggable database E4A open;
alter pluggable database E4B open;
alter pluggable database E4C open;
alter pluggable database E4I open;
select name,open_mode from v$pdbs;
exit
