-- Explicit post-delivery test data for the later upgrade; never packaged business seed.
whenever oserror exit failure rollback
whenever sqlerror exit failure rollback
set serveroutput on
declare n number; h number; w number; greeting varchar2(32767); session_id number;
begin
  if user<>'E1_UAT' then raise_application_error(-20750,'Retained user_acceptance_test fixture only'); end if;
  select count(*) into n from lab_components where component in ('Foundation','Hello','World') and installed=1 and version='1.0.0';
  if n<>3 then raise_application_error(-20751,'Initial complete release required for these sentinels'); end if;
  lab_runtime.assert_ready;
  select count(*) into n from greeting_history where actor='VERIFIER' and greeting_text='Hello World';
  if n<20 then
    -- Explicit selections: operator configuration/defaults must remain unchanged.
    select min(entry_id) into h from hello_entries where trim(entry_text)='Hello' and active='Y';
    select min(entry_id) into w from world_entries where trim(entry_text)='World' and active='Y';
    if h is null or w is null then
      raise_application_error(-20753,'Upgrade examples need active Hello and World entries; create them in UAT and resume examples. Existing settings are preserved.');
    end if;
    apex_util.set_workspace('E1_UAT');
    apex_session.create_session(p_app_id=>810005,p_page_id=>1,p_username=>'VERIFIER');
    session_id:=apex_application.g_instance;
    for i in 1..(20-n) loop
      greeting:=lab_runtime.record_greeting(h,w);
      if greeting<>'Hello World' then raise_application_error(-20752,'Upgrade examples require empty Hello/World prefixes for Hello World; examples rolled back, existing settings preserved'); end if;
    end loop;
    commit;
    apex_session.delete_session(p_session_id=>session_id);
  end if;
  dbms_output.put_line('PASS at least twenty verifier snapshots retained for later upgrade comparisons. Existing history unchanged; fixture is repeatable.');
exception when others then
  rollback;
  if session_id is not null then
    begin apex_session.delete_session(p_session_id=>session_id); exception when others then null; end;
  end if;
  raise;
end;
/
