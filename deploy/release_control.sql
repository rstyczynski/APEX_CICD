whenever oserror exit failure rollback
whenever sqlerror exit failure rollback
set serveroutput on
declare n number;
begin
  if user<>'E1_CTRL' then raise_application_error(-20610,'Control schema required'); end if;
  select count(*) into n from user_tables where table_name='E1_RELEASE_TARGETS';
  if n=0 then
    execute immediate q'[create table e1_release_targets (
      schema_name varchar2(30) primary key, app_id number unique not null,
      epoch number default 0 not null, phase varchar2(20) default 'new' not null,
      artifact_hash varchar2(64), source_commit varchar2(40), config_hash varchar2(64),
      fingerprint varchar2(4000), owner_name varchar2(30))]';
    execute immediate q'[insert into e1_release_targets(schema_name,app_id) values ('E1_QUALIFY',810004)]';
    execute immediate q'[insert into e1_release_targets(schema_name,app_id) values ('E1_TEST',810005)]';
    execute immediate q'[create table e1_release_attempts (
      schema_name varchar2(30) not null, epoch number not null,
      artifact_hash varchar2(64) not null, source_commit varchar2(40) not null,
      config_hash varchar2(64) not null, starting_state varchar2(20) not null,
      outcome varchar2(20) not null, started_at timestamp with time zone default systimestamp,
      finished_at timestamp with time zone, fingerprint varchar2(4000),
      primary key(schema_name,epoch))]';
    execute immediate q'[create table e1_qualified_artifacts (
      artifact_hash varchar2(64) primary key, source_commit varchar2(40) not null,
      config_hash varchar2(64) not null, qualification_epoch number not null,
      starting_state varchar2(20) not null, qualified_at timestamp with time zone default systimestamp)]';
    commit;
  end if;
  select count(*) into n from user_tab_columns where table_name='E1_RELEASE_ATTEMPTS' and column_name='FAILURE_REASON';
  if n=0 then execute immediate 'alter table e1_release_attempts add (failure_reason varchar2(1000))'; end if;
end;
/
create or replace package e1_release authid definer as
  procedure begin_initial(p_expected_epoch number,p_hash varchar2,p_commit varchar2,p_config varchar2);
  procedure assert_attempt(p_epoch number,p_hash varchar2);
  procedure verifying(p_epoch number,p_hash varchar2);
  procedure publish_initial(p_epoch number,p_hash varchar2,p_fingerprint varchar2);
  procedure show_status;
  procedure assert_runtime;
  procedure retire_disposable_qualification(p_epoch number,p_hash varchar2,p_reason varchar2);
end;
/
create or replace package body e1_release as
  function actor return varchar2 is v varchar2(30):=sys_context('USERENV','SESSION_USER');
  begin
    if v not in ('E1_QUALIFY','E1_TEST') then raise_application_error(-20611,'Not a controlled release identity'); end if;
    return v;
  end;
  procedure begin_initial(p_expected_epoch number,p_hash varchar2,p_commit varchar2,p_config varchar2) is
    who varchar2(30):=actor; r e1_release_targets%rowtype; n number;
  begin
    if not regexp_like(p_hash,'^[0-9a-f]{64}$') or p_hash is null or
       not regexp_like(p_commit,'^[0-9a-f]{40}$') or p_commit is null or
       not regexp_like(p_config,'^[0-9a-f]{64}$') or p_config is null then
      raise_application_error(-20612,'Full artifact/source/config identities required');
    end if;
    select * into r from e1_release_targets where schema_name=who for update nowait;
    if r.epoch<>p_expected_epoch or r.owner_name is not null or r.phase not in ('new','ready') then
      raise_application_error(-20613,'Stale epoch, active or interrupted attempt; inspect before recovery');
    end if;
    if who='E1_TEST' then
      select count(*) into n from e1_qualified_artifacts where artifact_hash=p_hash and source_commit=p_commit and config_hash=p_config and starting_state='empty';
      if n<>1 then raise_application_error(-20614,'No matching empty-target qualification for these exact bytes/configuration'); end if;
    end if;
    update e1_release_targets set epoch=epoch+1,phase='installing',owner_name=who,
      artifact_hash=p_hash,source_commit=p_commit,config_hash=p_config,fingerprint=null where schema_name=who;
    insert into e1_release_attempts(schema_name,epoch,artifact_hash,source_commit,config_hash,starting_state,outcome)
      values(who,r.epoch+1,p_hash,p_commit,p_config,'empty','installing');
    commit;
    dbms_output.put_line('ADMITTED INITIAL ATTEMPT epoch '||(r.epoch+1)||'; durable ownership survives disconnects and DDL commits.');
  exception when others then rollback; raise;
  end;
  procedure assert_attempt(p_epoch number,p_hash varchar2) is who varchar2(30):=actor; n number;
  begin
    select count(*) into n from e1_release_targets where schema_name=who and owner_name=who and epoch=p_epoch and artifact_hash=p_hash and phase in ('installing','verifying');
    if n<>1 then raise_application_error(-20615,'Missing or stale release ownership'); end if;
  end;
  procedure verifying(p_epoch number,p_hash varchar2) is who varchar2(30):=actor;
  begin
    assert_attempt(p_epoch,p_hash);
    update e1_release_targets set phase='verifying' where schema_name=who and phase='installing';
    if sql%rowcount<>1 then raise_application_error(-20621,'Only installed attempts enter verification'); end if;
    update e1_release_attempts set outcome='verifying' where schema_name=who and epoch=p_epoch;
    -- Caller commits atomically with restricted native availability.
  end;
  procedure publish_initial(p_epoch number,p_hash varchar2,p_fingerprint varchar2) is
    who varchar2(30):=actor; r e1_release_targets%rowtype;
  begin
    assert_attempt(p_epoch,p_hash);
    select * into r from e1_release_targets where schema_name=who for update nowait;
    if r.phase<>'verifying' or p_fingerprint is null or not regexp_like(p_fingerprint,'^SH256:[A-Za-z0-9+/]{43}=$') then raise_application_error(-20616,'Verification and final fingerprint required'); end if;
    if who='E1_QUALIFY' then
      insert into e1_qualified_artifacts(artifact_hash,source_commit,config_hash,qualification_epoch,starting_state)
        values(r.artifact_hash,r.source_commit,r.config_hash,r.epoch,'empty');
    end if;
    update e1_release_attempts set outcome='succeeded',finished_at=systimestamp,fingerprint=p_fingerprint where schema_name=who and epoch=p_epoch;
    update e1_release_targets set phase='ready',owner_name=null,fingerprint=p_fingerprint where schema_name=who;
    -- No commit: root readiness/native availability/receipt publish together.
  end;
  procedure assert_runtime is
    app number:=apex_application.g_flow_id; phase varchar2(20);
  begin
    -- The three private authoring checkpoints are not controlled release targets.
    if app in (810001,810002,810003) then return; end if;
    select t.phase into phase from e1_release_targets t where t.app_id=app;
    -- Login can authenticate the verifier; all business pages still check below.
    if apex_application.g_flow_step_id=9999 then return; end if;
    if phase='ready' then return; end if;
    if phase='verifying' and upper(apex_application.g_user)='VERIFIER' then return; end if;
    raise_application_error(-20631,'Release verification in progress: ordinary application access is blocked.');
  exception when no_data_found then
    raise_application_error(-20632,'Missing controlled-target state: application access blocked.');
  end;
  procedure retire_disposable_qualification(p_epoch number,p_hash varchar2,p_reason varchar2) is
    who varchar2(30):=actor;
  begin
    if who<>'E1_QUALIFY' or p_reason is null or length(p_reason)<20 then
      raise_application_error(-20633,'Only an inspected disposable qualification attempt may be retired');
    end if;
    assert_attempt(p_epoch,p_hash);
    update e1_release_attempts set outcome='failed',finished_at=systimestamp,failure_reason=p_reason where schema_name=who and epoch=p_epoch;
    update e1_release_targets set phase='new',owner_name=null where schema_name=who;
    commit;
  end;
  procedure show_status is r e1_release_targets%rowtype; who varchar2(30):=actor;
  begin
    select * into r from e1_release_targets where schema_name=who;
    dbms_output.put_line('TARGET='||r.schema_name||' APP='||r.app_id||' EPOCH='||r.epoch||' PHASE='||r.phase);
    dbms_output.put_line('ARTIFACT='||r.artifact_hash);
    dbms_output.put_line('SOURCE='||r.source_commit);
    dbms_output.put_line('CONFIG='||r.config_hash);
    dbms_output.put_line('FINGERPRINT='||r.fingerprint);
  end;
end;
/
grant execute on e1_release to E1_QUALIFY, E1_TEST, E1_DEV_A, E1_DEV_B, E1_DEV_C;
select name,type,line,text from user_errors where name='E1_RELEASE';
declare n number;
begin
 select count(*) into n from user_errors where name='E1_RELEASE';
 if n<>0 then raise_application_error(-20617,'Release control compilation failed'); end if;
end;
/
