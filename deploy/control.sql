set serveroutput on
declare n number;
begin
  select count(*) into n from user_tables where table_name='E1_COORDINATION';
  if n=0 then
    execute immediate 'create table e1_coordination (id number primary key, next_generation number not null)';
    execute immediate 'insert into e1_coordination values (1,0)';
    execute immediate 'create table e1_reservations (component varchar2(20) primary key, owner_name varchar2(128), task_id varchar2(80), base_revision varchar2(40), generation number)';
    execute immediate q'[insert into e1_reservations(component) values ('Foundation')]';
    execute immediate q'[insert into e1_reservations(component) values ('Hello')]';
    execute immediate q'[insert into e1_reservations(component) values ('World')]';
    execute immediate 'create table e1_control_events (event_id number generated always as identity primary key, occurred_at timestamp with time zone default systimestamp not null, actor varchar2(128) not null, action varchar2(20) not null, task_id varchar2(80), generation number, scope varchar2(80))';
    commit;
  end if;
end;
/
create or replace package e1_ownership authid definer as
  function acquire(p_scope varchar2,p_task varchar2,p_base varchar2) return number;
  procedure assert_owned(p_component varchar2,p_task varchar2,p_generation number);
  procedure release_task(p_task varchar2,p_generation number);
end;
/
create or replace package body e1_ownership as
  function actor return varchar2 is
    v varchar2(128):=sys_context('USERENV','SESSION_USER');
  begin
    if v not in ('E1_DEV_A','E1_DEV_B','E1_DEV_C') then
      raise_application_error(-20100,'Not a registered developer');
    end if;
    return v;
  end;
  function acquire(p_scope varchar2,p_task varchar2,p_base varchar2) return number is
    v_actor varchar2(128):=actor;
    v_generation number;
    v_count number;
    v_conflict varchar2(300);
  begin
    if p_task is null or length(p_task)>80 or p_base is null or not regexp_like(p_base,'^[0-9a-f]{40}$') then
      raise_application_error(-20101,'Task and full base revision are required');
    end if;
    if p_scope is null or not regexp_like(p_scope,'^(Foundation|Hello|World)(,(Foundation|Hello|World))*$') then
      raise_application_error(-20102,'Unknown component scope');
    end if;
    select next_generation into v_generation from e1_coordination where id=1 for update nowait;
    select count(*) into v_count from e1_reservations
      where instr(','||p_scope||',',','||component||',')>0 and owner_name is not null;
    if v_count>0 then
      select min(component||' owned by '||owner_name||' task '||task_id) into v_conflict
        from e1_reservations where instr(','||p_scope||',',','||component||',')>0 and owner_name is not null;
      raise_application_error(-20103,v_conflict);
    end if;
    v_generation:=v_generation+1;
    update e1_coordination set next_generation=v_generation where id=1;
    update e1_reservations set owner_name=v_actor,task_id=p_task,base_revision=p_base,generation=v_generation
      where instr(','||p_scope||',',','||component||',')>0;
    insert into e1_control_events(actor,action,task_id,generation,scope)
      values(v_actor,'acquire',p_task,v_generation,p_scope);
    commit;
    return v_generation;
  exception when others then rollback; raise;
  end;
  procedure assert_owned(p_component varchar2,p_task varchar2,p_generation number) is
    v_actor varchar2(128):=actor;
    n number;
  begin
    select count(*) into n from e1_reservations where component=p_component and owner_name=v_actor
      and task_id=p_task and generation=p_generation;
    if n<>1 then raise_application_error(-20104,'Task does not own this component/generation'); end if;
  end;
  procedure release_task(p_task varchar2,p_generation number) is
    v_actor varchar2(128):=actor;
    n number;
  begin
    select next_generation into n from e1_coordination where id=1 for update nowait;
    update e1_reservations set owner_name=null,task_id=null,base_revision=null
      where owner_name=v_actor and task_id=p_task and generation=p_generation;
    if sql%rowcount=0 then raise_application_error(-20105,'No matching owned task to release'); end if;
    insert into e1_control_events(actor,action,task_id,generation) values(v_actor,'release',p_task,p_generation);
    commit;
  exception when others then rollback; raise;
  end;
end;
/
declare n number; begin
  select count(*) into n from user_errors where name='E1_OWNERSHIP';
  if n>0 then raise_application_error(-20106,'Control package compilation failed'); end if;
end;
/
