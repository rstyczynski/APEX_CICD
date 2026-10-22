declare n number;
begin
 select count(*) into n from user_tab_columns where table_name='E2_SETTINGS' and column_name='RELEASE_NOTE';
 if n=0 then execute immediate 'alter table e2_settings add (release_note varchar2(50))'; end if;
end;
/
@@patch.sql
