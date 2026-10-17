-- Explicit post-delivery test data for the later upgrade; never packaged business seed.
whenever oserror exit failure rollback
whenever sqlerror exit failure rollback
set serveroutput on
declare n number; greeting varchar2(32767); session_id number;
begin
  if user<>'E1_TEST' then raise_application_error(-20750,'Retained TEST fixture only'); end if;
  select count(*) into n from lab_components where component in ('Foundation','Hello','World') and installed=1 and version='1.0.0';
  if n<>3 then raise_application_error(-20751,'Initial complete release required for these sentinels'); end if;
  lab_runtime.assert_ready;
  select count(*) into n from greeting_history where actor='VERIFIER' and greeting_text='Hello World';
  if n<20 then
    apex_util.set_workspace('E1_TEST');
    apex_session.create_session(p_app_id=>810005,p_page_id=>1,p_username=>'VERIFIER');
    session_id:=apex_application.g_instance;
    for i in 1..(20-n) loop
      greeting:=lab_runtime.record_greeting;
      if greeting<>'Hello World' then raise_application_error(-20752,'Fixture defaults changed; rollback'); end if;
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
