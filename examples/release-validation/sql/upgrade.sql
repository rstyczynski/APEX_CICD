declare n number; begin
 select count(*) into n from dba_tab_columns where owner='E7_APP' and table_name='GREETINGS' and column_name='LANGUAGE_CODE';
 if n=0 then execute immediate 'alter table e7_app.greetings add language_code varchar2(2) default ''en'' not null'; end if;
 select count(*) into n from dba_constraints where owner='E7_APP' and constraint_name='E7_LANGUAGE_CK';
 if n=0 then execute immediate 'alter table e7_app.greetings add constraint e7_language_ck check(language_code in (''en'',''pl''))'; end if;
end;
/
create or replace package body e7_app.greeting_api as function render(p_text varchar2) return varchar2 is begin return 'Hello '||trim(p_text); end; end;
/
merge into e7_app.migrations d using(select '1.1.0' version from dual) s on(d.version=s.version) when not matched then insert(version) values(s.version);
commit;
