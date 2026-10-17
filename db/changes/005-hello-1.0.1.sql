-- Compatible correction: normalize all surrounding whitespace, not only spaces.
-- No existing entries, defaults, prefixes or history are rewritten.
alter table hello_entries add constraint hello_text_nonblank
  check (regexp_like(entry_text,'[^[:space:]]'))
/
create or replace trigger hello_entries_guard
before insert or update on hello_entries for each row
declare n number;
begin
  lab_runtime.assert_ready;
  :new.entry_text:=regexp_replace(:new.entry_text,'^[[:space:]]+|[[:space:]]+$','');
  if :new.entry_text is null then raise_application_error(-20314,'Hello entry must contain non-whitespace text'); end if;
  if :new.active='N' then
    select count(*) into n from hello_config where default_entry_id=:new.entry_id;
    if n>0 then raise_application_error(-20310,'Choose another active Hello default before deactivation'); end if;
  end if;
end;
/
update lab_components set version='1.0.1' where component='Hello'
/
