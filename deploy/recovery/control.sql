whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
set serveroutput on
declare n number;
begin
 if user<>'E1_CTRL' then raise_application_error(-20840,'Control owner required'); end if;
 select count(*) into n from user_tables where table_name='E1_RECOVERY_CASES';
 if n=0 then
 execute immediate q'[create table e1_recovery_cases(
  failed_epoch number primary key, repair_epoch number, failed_hash varchar2(64) not null,
  repair_hash varchar2(64), previous_hash varchar2(64), previous_fingerprint varchar2(4000),
  config_hash varchar2(64), observation varchar2(4000), phase varchar2(20) not null,
  repair_observation varchar2(4000))]';
 end if;
end;
/
create or replace package e1_recovery authid definer as
 procedure start_failure(p_epoch number,p_hash varchar2,p_source varchar2,p_expected_hash varchar2,p_fingerprint varchar2);
 procedure record_failure(p_epoch number,p_hash varchar2,p_observation varchar2);
 procedure start_repair(p_failed_epoch number,p_hash varchar2,p_source varchar2,p_observation varchar2);
 procedure finish_repair(p_failed_epoch number,p_hash varchar2,p_observation varchar2,p_fingerprint varchar2);
end;
/
create or replace package body e1_recovery as
 procedure actor is begin
  if sys_context('USERENV','SESSION_USER')<>'E1_INTEGRATION' then raise_application_error(-20841,'Recovery experiment is integration-only'); end if;
 end;
 procedure identities(p_hash varchar2,p_source varchar2) is begin
  if p_hash is null or not regexp_like(p_hash,'^[0-9a-f]{64}$') or p_source is null or not regexp_like(p_source,'^[0-9a-f]{40}$') then
   raise_application_error(-20842,'Full archive/source identities required'); end if;
 end;
 procedure start_failure(p_epoch number,p_hash varchar2,p_source varchar2,p_expected_hash varchar2,p_fingerprint varchar2) is
  r e1_release_targets%rowtype;
 begin
  actor; identities(p_hash,p_source);
  select * into r from e1_release_targets where schema_name='E1_INTEGRATION' for update nowait;
  if r.phase<>'ready' or r.owner_name is not null or r.epoch<>p_epoch or r.artifact_hash<>p_expected_hash or
   r.fingerprint is null or p_fingerprint is null or r.fingerprint<>p_fingerprint then raise_application_error(-20843,'Recovery baseline is active, stale or drifted'); end if;
  insert into e1_recovery_cases(failed_epoch,failed_hash,previous_hash,previous_fingerprint,config_hash,phase)
   values(r.epoch+1,p_hash,r.artifact_hash,r.fingerprint,r.config_hash,'installing');
  update e1_release_targets set epoch=epoch+1,phase='installing',owner_name='E1_INTEGRATION',artifact_hash=p_hash,source_commit=p_source,fingerprint=null
   where schema_name='E1_INTEGRATION';
  insert into e1_release_attempts(schema_name,epoch,artifact_hash,source_commit,config_hash,starting_state,outcome)
   values('E1_INTEGRATION',r.epoch+1,p_hash,p_source,r.config_hash,'1.0.1','installing');
  commit;
 end;
 procedure record_failure(p_epoch number,p_hash varchar2,p_observation varchar2) is
 begin
  actor; e1_release.assert_attempt(p_epoch,p_hash);
  if p_observation is null then raise_application_error(-20844,'Partial observation required'); end if;
  update e1_release_attempts set outcome='failed',finished_at=systimestamp,failure_reason='BUG-7: committed actor index; deliberate ORA-20831'
   where schema_name='E1_INTEGRATION' and epoch=p_epoch;
  update e1_recovery_cases set phase='failed',observation=p_observation where failed_epoch=p_epoch and failed_hash=p_hash and phase='installing';
  if sql%rowcount<>1 then raise_application_error(-20845,'Failure case mismatch'); end if;
  update e1_release_targets set phase='failed' where schema_name='E1_INTEGRATION';
  commit;
 end;
 procedure start_repair(p_failed_epoch number,p_hash varchar2,p_source varchar2,p_observation varchar2) is
  r e1_release_targets%rowtype; c e1_recovery_cases%rowtype;
 begin
  actor; identities(p_hash,p_source);
  select * into r from e1_release_targets where schema_name='E1_INTEGRATION' for update nowait;
  select * into c from e1_recovery_cases where failed_epoch=p_failed_epoch for update;
  if r.phase<>'failed' or r.epoch<>p_failed_epoch or r.owner_name<>'E1_INTEGRATION' or r.artifact_hash<>c.failed_hash or c.phase<>'failed' or
    p_observation is null or c.observation<>p_observation then raise_application_error(-20846,'Partial state changed or repair authority stale'); end if;
  update e1_recovery_cases set repair_epoch=r.epoch+1,repair_hash=p_hash,phase='repairing' where failed_epoch=p_failed_epoch;
  update e1_release_targets set epoch=epoch+1,phase='installing',artifact_hash=p_hash,source_commit=p_source where schema_name='E1_INTEGRATION';
  insert into e1_release_attempts(schema_name,epoch,artifact_hash,source_commit,config_hash,starting_state,outcome)
   values('E1_INTEGRATION',r.epoch+1,p_hash,p_source,r.config_hash,'BUG7-partial','installing');
  commit;
 end;
 procedure finish_repair(p_failed_epoch number,p_hash varchar2,p_observation varchar2,p_fingerprint varchar2) is
  c e1_recovery_cases%rowtype;
 begin
  actor;
  select * into c from e1_recovery_cases where failed_epoch=p_failed_epoch for update;
  e1_release.assert_attempt(c.repair_epoch,p_hash);
  if c.phase<>'repairing' or c.repair_hash<>p_hash or p_observation is null or p_fingerprint is null or p_fingerprint<>c.previous_fingerprint then
   raise_application_error(-20847,'Repair completion identity/fingerprint mismatch'); end if;
  update e1_recovery_cases set phase='repaired',repair_observation=p_observation where failed_epoch=p_failed_epoch;
  update e1_release_attempts set outcome='succeeded',finished_at=systimestamp,fingerprint=p_fingerprint
   where schema_name='E1_INTEGRATION' and epoch=c.repair_epoch and artifact_hash=p_hash;
  update e1_release_targets set phase='ready',owner_name=null,fingerprint=p_fingerprint where schema_name='E1_INTEGRATION';
  -- Caller opens its lab_state gate in this same final transaction.
 end;
end;
/
declare n number; begin
 select count(*) into n from user_errors where name='E1_RECOVERY';
 if n<>0 then raise_application_error(-20848,'Recovery authority compilation failed'); end if;
end;
/
grant execute on e1_recovery to E1_INTEGRATION;
grant select on e1_recovery_cases to E1_INTEGRATION;
