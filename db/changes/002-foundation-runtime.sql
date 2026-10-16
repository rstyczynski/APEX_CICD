-- Foundation owns composition and snapshots. Component tables arrive later.
create or replace package lab_runtime authid definer as
  procedure assert_ready;
  function record_greeting(p_hello_id number default null, p_world_id number default null) return varchar2;
end;
/
create or replace package body lab_runtime as
  procedure assert_ready is
    v_state varchar2(20);
    n number;
  begin
    -- Serializes admitted mutations with the transition into maintenance.
    select state into v_state from lab_state where state_key='Application' for update nowait;
    if v_state <> 'ready' or v_state is null then
      raise_application_error(-20300,'Application is unavailable: assembly or maintenance');
    end if;
    select count(*) into n from lab_state where state_key in ('Foundation','Hello','World') and state='ready';
    if n<>3 then raise_application_error(-20301,'A required component is unavailable'); end if;
    select count(*) into n from lab_components where installed=1 and
      ((component='Foundation' and version='1.0.0') or
       (component='Hello' and version in ('1.0.0','1.0.1')) or
       (component='World' and version='1.0.0'));
    if n<>3 then raise_application_error(-20302,'Unsupported installed component versions'); end if;
  end;
  function record_greeting(p_hello_id number default null, p_world_id number default null) return varchar2 is
    h_id number; w_id number;
    h_text varchar2(100 char); w_text varchar2(100 char);
    h_prefix varchar2(30 char); w_prefix varchar2(30 char);
    greeting varchar2(261 char);
    who varchar2(255 char):=coalesce(apex_application.g_user,sys_context('USERENV','SESSION_USER'));
  begin
    assert_ready;
    if who is null or upper(who) in ('NOBODY','APEX_PUBLIC_USER','ANONYMOUS') then
      raise_application_error(-20303,'An authenticated user is required');
    end if;
    execute immediate 'select e.entry_id,e.entry_text,c.prefix from hello_entries e cross join hello_config c where c.config_id=1 and e.entry_id=coalesce(:id,c.default_entry_id) and e.active=''Y'''
      into h_id,h_text,h_prefix using p_hello_id;
    execute immediate 'select e.entry_id,e.entry_text,c.prefix from world_entries e cross join world_config c where c.config_id=1 and e.entry_id=coalesce(:id,c.default_entry_id) and e.active=''Y'''
      into w_id,w_text,w_prefix using p_world_id;
    greeting:=h_prefix||trim(h_text)||' '||w_prefix||trim(w_text);
    insert into greeting_history(hello_entry_id,world_entry_id,hello_text,world_text,hello_prefix,world_prefix,greeting_text,actor)
      values(h_id,w_id,trim(h_text),trim(w_text),h_prefix,w_prefix,greeting,who);
    return greeting;
  exception when no_data_found then
    raise_application_error(-20304,'Select active Hello and World entries or configure active defaults');
  end;
end;
/
create or replace trigger greeting_history_immutable
before update or delete on greeting_history
begin
  raise_application_error(-20305,'Greeting history is immutable');
end;
/
create or replace trigger greeting_history_insert_guard
before insert on greeting_history
begin
  lab_runtime.assert_ready;
end;
/
