-- Reviewed Hello 1.0.1 authoring input: surrounding-whitespace correction.
-- Schema DDL is shared by all Working Copies; apply once to the author schema.
-- No existing entries, prefixes, defaults or greeting history are rewritten.
set serveroutput on

declare
  l_count number;
  l_version varchar2(30);
begin
  if user <> 'E1_DEV_C' then
    raise_application_error(-20880,'Hello authoring input requires E1_DEV_C');
  end if;
  select count(*) into l_count from lab_components
    where installed=1 and ((component in ('Foundation','World') and version='1.0.0')
      or (component='Hello' and version in ('1.0.0','1.0.1')));
  if l_count<>3 then raise_application_error(-20881,'Unsupported component baseline'); end if;
  select version into l_version from lab_components where component='Hello';
  select count(*) into l_count from user_constraints
    where table_name='HELLO_ENTRIES' and constraint_name='HELLO_TEXT_NONBLANK';
  if l_version='1.0.1' then
    if l_count<>1 then raise_application_error(-20882,'Version/constraint mismatch; inspect'); end if;
    dbms_output.put_line('Hello 1.0.1 authoring input already applied; inspect definitions below.');
    return;
  end if;
  if l_count<>0 then raise_application_error(-20882,'Unexpected existing constraint; inspect'); end if;
  execute immediate q'~alter table hello_entries add constraint hello_text_nonblank
    check (regexp_like(entry_text,'[^[:space:]]'))~';
  execute immediate q'~create or replace trigger hello_entries_guard
before insert or update on hello_entries for each row
declare n number;
begin
  lab_runtime.assert_ready;
  :new.entry_text:=regexp_replace(:new.entry_text,'^[[:space:]]+|[[:space:]]+$','');
  if :new.entry_text is null then
    raise_application_error(-20314,'Hello entry must contain non-whitespace text');
  end if;
  if :new.active='N' then
    select count(*) into n from hello_config where default_entry_id=:new.entry_id;
    if n>0 then raise_application_error(-20310,'Choose another active Hello default before deactivation'); end if;
  end if;
end;~';
  select count(*) into l_count from user_errors where name='HELLO_ENTRIES_GUARD';
  if l_count<>0 then raise_application_error(-20883,'Hello trigger compilation failed; inspect errors'); end if;
  update lab_components set version='1.0.1' where component='Hello';
  commit;
  dbms_output.put_line('PASS Hello 1.0.1 authoring correction applied; retained data not rewritten.');
end;
/
select component, installed, version from lab_components order by component;
select constraint_name,status,validated from user_constraints
 where table_name='HELLO_ENTRIES' and constraint_name='HELLO_TEXT_NONBLANK';
select text from user_source where name='HELLO_ENTRIES_GUARD' and type='TRIGGER' order by line;
