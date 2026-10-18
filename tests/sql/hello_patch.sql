-- Transactional validation of the compatible correction; no business seed.
set serveroutput on
declare entry number; value varchar2(100); rejected boolean:=false;
begin
 savepoint patch_assertions;
 update lab_state set state='ready' where state_key='Application';
 insert into hello_entries(entry_text,active) values(chr(9)||'Patched Hello'||chr(10),'Y') returning entry_id into entry;
 select entry_text into value from hello_entries where entry_id=entry;
 if value<>'Patched Hello' then raise_application_error(-20770,'All surrounding whitespace must normalize'); end if;
 begin
  insert into hello_entries(entry_text,active) values(chr(9)||chr(10),'Y');
 exception when others then
  if sqlcode=-20314 then rejected:=true; else raise; end if;
 end;
 if not rejected then raise_application_error(-20771,'Whitespace-only Hello must reject specifically'); end if;
 rollback to patch_assertions;
 dbms_output.put_line('PASS Hello 1.0.1 whitespace normalization and specific blank rejection; fixtures rolled back.');
exception when others then rollback; raise;
end;
/
