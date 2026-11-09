-- New, empty E4 fixture only; never run on the retained lab or central target.
-- This is fixture preparation, not a release migration or edited historical guard.
declare
  n number;
  h number;
  w number;
begin
  if user <> 'E1_DEV_C' or sys_context('USERENV','CON_NAME') <> 'E4A' then
    raise_application_error(-20940,'Expected new E4A author fixture');
  end if;
  select sum(n) into n from (
    select count(*) n from lab_components union all select count(*) from lab_state
    union all select count(*) from hello_entries union all select count(*) from world_entries
    union all select count(*) from hello_config union all select count(*) from world_config
    union all select count(*) from greeting_history);
  if n <> 0 then raise_application_error(-20941,'Fixture must be empty'); end if;
  insert into lab_components values ('Foundation',1,'1.0.0');
  insert into lab_components values ('Hello',1,'1.0.0');
  insert into lab_components values ('World',1,'1.0.0');
  insert into lab_state values ('Application',null,'ready','E4 literal fixture');
  insert into lab_state values ('Foundation','Application','ready','E4 literal fixture');
  insert into lab_state values ('Hello','Application','ready','E4 literal fixture');
  insert into lab_state values ('World','Application','ready','E4 literal fixture');
  insert into hello_entries(entry_text,active) values ('Hello','Y') returning entry_id into h;
  insert into world_entries(entry_text,active) values ('World','Y') returning entry_id into w;
  insert into hello_config values (1,null,h);
  insert into world_config values (1,null,w);
  commit;
end;
/
