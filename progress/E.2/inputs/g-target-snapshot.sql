-- Read-only target evidence; no migration, publication or business inserts.
set serveroutput on size unlimited
set feedback off
set heading off
set pagesize 0
set long 10000000
set longchunksize 10000000
set linesize 32767
declare
  files apex_t_export_files;
  value_clob clob;
  procedure emit(v clob) is p number:=1; begin
    while p<=dbms_lob.getlength(v) loop
      dbms_output.put_line(dbms_lob.substr(v,4000,p)); p:=p+4000;
    end loop;
  end;
begin
  if user<>'E1_UAT' then raise_application_error(-20897,'G requires E1_UAT'); end if;
  dbms_output.put_line('TARGET|'||sys_context('USERENV','DB_UNIQUE_NAME')||'|'||sys_context('USERENV','CON_NAME')||'|'||user||'|810005');
  for r in (select table_name from user_tables where table_name in
    ('GREETING_HISTORY','HELLO_ENTRIES','WORLD_ENTRIES','HELLO_CONFIG','WORLD_CONFIG',
     'LAB_COMPONENTS','LAB_STATE','DATABASECHANGELOG','DATABASECHANGELOGLOCK') order by table_name) loop
    dbms_output.put_line('TABLE|'||r.table_name);
    execute immediate 'select coalesce(json_arrayagg(row_json order by row_json returning clob),to_clob(''[]'')) from (select json_object(*) row_json from '||r.table_name||')' into value_clob;
    emit(value_clob);
  end loop;
  for r in (select object_name,object_type from user_objects where object_type in
      ('TABLE','TRIGGER','PACKAGE','PACKAGE BODY','VIEW') order by object_type,object_name) loop
    dbms_output.put_line('DDL|'||r.object_type||'|'||r.object_name);
    emit(dbms_metadata.get_ddl(replace(r.object_type,' ','_'),r.object_name));
  end loop;
  apex_util.set_workspace('E1_UAT');
  files:=apex_export.get_application(p_application_id=>810005,p_with_date=>false);
  for i in 1..files.count loop
    dbms_output.put_line('APEX|'||files(i).name); emit(files(i).contents);
  end loop;
  for r in (select availability_status from apex_applications where application_id=810005) loop
    dbms_output.put_line('STATUS|'||r.availability_status);
  end loop;
end;
/
