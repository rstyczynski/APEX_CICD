-- E2_INITIAL_RELEASE_DATA_1_0_0
-- Append below the generated custom changeset header, once, before first use.
-- Fixed demonstration inputs; no SELECT from a developer or retained schema.
-- Initial installation only. Liquibase owns the transaction and execution history.
declare
  l_existing number;
  l_hello_id number;
  l_world_id number;
begin
  if user not in ('E1_INTEGRATION', 'E1_UAT') then
    raise_application_error(-20860, 'Initial release data requires an owned delivery target');
  end if;

  select sum(n) into l_existing from (
    select count(*) n from lab_components union all
    select count(*) from lab_state union all
    select count(*) from hello_entries union all
    select count(*) from hello_config union all
    select count(*) from world_entries union all
    select count(*) from world_config union all
    select count(*) from greeting_history
  );
  if l_existing <> 0 then
    raise_application_error(-20861, 'Initial release data refuses a populated target');
  end if;

  insert into lab_components(component, installed, version) values ('Foundation', 1, '1.0.0');
  insert into lab_components(component, installed, version) values ('Hello', 1, '1.0.0');
  insert into lab_components(component, installed, version) values ('World', 1, '1.0.0');

  insert into lab_state(state_key, parent_key, state, reason)
    values ('Application', null, 'ready', 'Initial demonstration assembly');
  insert into lab_state(state_key, parent_key, state, reason)
    values ('Foundation', 'Application', 'ready', 'Foundation 1.0.0 installed');
  insert into lab_state(state_key, parent_key, state, reason)
    values ('Hello', 'Application', 'ready', 'Hello 1.0.0 installed');
  insert into lab_state(state_key, parent_key, state, reason)
    values ('World', 'Application', 'ready', 'World 1.0.0 installed');

  -- These two new literal examples make the delivered demonstration usable.
  -- They are not exported author data or retained user settings/history.
  insert into hello_entries(entry_text, active) values ('Hello', 'Y')
    returning entry_id into l_hello_id;
  insert into world_entries(entry_text, active) values ('World', 'Y')
    returning entry_id into l_world_id;
  insert into hello_config(config_id, prefix, default_entry_id)
    values (1, null, l_hello_id);
  insert into world_config(config_id, prefix, default_entry_id)
    values (1, null, l_world_id);
end;
/
