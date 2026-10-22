-- Read component/schema state and exercise Hello 1.0.1 in a rolled-back transaction.
set serveroutput on
declare
  l_count number;
  l_text varchar2(100);
begin
  if user not in ('E1_DEV_C','E1_INTEGRATION','E1_UAT') then
    raise_application_error(-20891,'Wrong Hello verification schema');
  end if;
  select count(*) into l_count from lab_components where installed=1 and
    ((component in ('Foundation','World') and version='1.0.0') or
     (component='Hello' and version='1.0.1'));
  if l_count<>3 then raise_application_error(-20892,'Expected Foundation 1.0.0 / Hello 1.0.1 / World 1.0.0'); end if;
  select count(*) into l_count from user_objects where status='INVALID'
    and object_type in ('PACKAGE','PACKAGE BODY','TRIGGER');
  if l_count<>0 then raise_application_error(-20893,'Invalid application code'); end if;
  savepoint f2_verify;
  insert into hello_entries(entry_text,active) values(chr(9)||'Hello'||chr(10),'Y')
    returning entry_text into l_text;
  if l_text<>'Hello' or l_text is null then
    raise_application_error(-20894,'Surrounding whitespace was not normalized');
  end if;
  rollback to f2_verify;
  begin
    insert into hello_entries(entry_text,active) values(chr(9)||chr(10),'Y');
    raise_application_error(-20895,'Whitespace-only Hello was accepted');
  exception when others then
    if sqlcode<>-20314 then raise; end if;
    dbms_output.put_line('PASS whitespace-only Hello rejected with ORA-20314');
  end;
  rollback to f2_verify;
  dbms_output.put_line('PASS Hello 1.0.1 normalization; verification inserts rolled back');
exception when others then
  rollback;
  raise;
end;
/
select component,installed,version from lab_components order by component;
