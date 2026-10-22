-- Explicitly reset only the disposable integration qualification area.
-- Usage in SQLcl: @.../f2-reset-integration.sql RESET_E1_INTEGRATION
-- Deletes its application and test data; leaves workspace/accounts/schema intact.
set define on
set verify off
set serveroutput on
declare
  l_count number;
begin
  if user<>'E1_INTEGRATION' or '&1'<>'RESET_E1_INTEGRATION' then
    raise_application_error(-20896,'Reset requires E1_INTEGRATION and the explicit reset token');
  end if;
  select count(*) into l_count from apex_applications
    where workspace='E1_INTEGRATION' and (application_id<>810004 or owner<>user);
  if l_count<>0 then raise_application_error(-20897,'Unexpected application in qualification workspace'); end if;
  select count(*) into l_count from user_tables where table_name not in
    ('GREETING_HISTORY','HELLO_CONFIG','WORLD_CONFIG','HELLO_ENTRIES','WORLD_ENTRIES',
     'LAB_COMPONENTS','LAB_STATE','DATABASECHANGELOG','DATABASECHANGELOGLOCK','DATABASECHANGELOG_ACTIONS');
  if l_count<>0 then raise_application_error(-20898,'Unexpected table in qualification schema'); end if;
  select count(*) into l_count from apex_applications where application_id=810004;
  if l_count>0 then
    select count(*) into l_count from apex_applications
      where application_id=810004 and workspace='E1_INTEGRATION' and owner=user;
    if l_count<>1 then raise_application_error(-20897,'Application 810004 is not owned by this target'); end if;
    apex_application_install.set_workspace('E1_INTEGRATION');
    apex_application_install.set_keep_sessions(false);
    apex_application_install.remove_application(810004);
  end if;
  for r in (select object_name,object_type from user_objects
      where (object_type='PACKAGE' and object_name='LAB_RUNTIME') or
            (object_type='VIEW' and object_name='DATABASECHANGELOG_DETAILS')) loop
    execute immediate 'drop '||r.object_type||' '||dbms_assert.simple_sql_name(r.object_name);
  end loop;
  for r in (select table_name from user_tables where table_name in
    ('GREETING_HISTORY','HELLO_CONFIG','WORLD_CONFIG','HELLO_ENTRIES','WORLD_ENTRIES',
     'LAB_COMPONENTS','LAB_STATE','DATABASECHANGELOG','DATABASECHANGELOGLOCK','DATABASECHANGELOG_ACTIONS')) loop
    execute immediate 'drop table '||dbms_assert.simple_sql_name(r.table_name)||' cascade constraints purge';
  end loop;
  dbms_output.put_line('PASS disposable integration application and tables removed; UAT not touched');
end;
/
select count(*) as remaining_tables from user_tables;
select count(*) as remaining_application from apex_applications where application_id=810004;
