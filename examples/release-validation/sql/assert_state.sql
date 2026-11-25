declare n number;
 procedure require_state(ok boolean,label varchar2) is begin if not ok then raise_application_error(-20701,'STATE:'||label); end if; end;
begin
 select count(*) into n from dba_tab_columns where owner='E7_APP' and table_name='GREETINGS' and column_name='LANGUAGE_CODE' and data_type='VARCHAR2' and char_length=2 and nullable='N';
 require_state(n=1,'COLUMN');
 select count(*) into n from dba_constraints where owner='E7_APP' and constraint_name='E7_LANGUAGE_CK' and status='ENABLED' and validated='VALIDATED';
 require_state(n=1,'CONSTRAINT');
 select count(*) into n from dba_tab_privs where owner='E7_APP' and table_name='GREETING_API' and grantee='E7_CONSUMER' and privilege='EXECUTE';
 require_state(n=1,'GRANT');
 select count(*) into n from dba_objects where owner='E7_APP' and status<>'VALID';
 require_state(n=0,'INVALID_OBJECT');
 select count(*) into n from e7_app.release_reference where code='LANGUAGE' and value='en';
 require_state(n=1,'REFERENCE');
 select count(*) into n from e7_app.migrations where version='1.1.0';
 require_state(n=1,'HISTORY');
 require_state(e7_app.greeting_api.render(' World ')='Hello World','CONSUMER');
 dbms_output.put_line('E7_STATE_PASS');
end;
/
