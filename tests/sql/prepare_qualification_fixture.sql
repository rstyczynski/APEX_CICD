-- Explicit verification data after initial reconstruction, never part of a release import.
set serveroutput on
declare h number; w number; greeting varchar2(32767); session_id number; n number;
begin
 if user<>'E1_INTEGRATION' then raise_application_error(-20782,'Disposable qualification fixture only'); end if;
 select count(*) into n from greeting_history;
 if n<>0 then raise_application_error(-20783,'Fresh reconstructed baseline required; fixture never overwrites'); end if;
 apex_util.set_workspace('E1_INTEGRATION');
 apex_session.create_session(p_app_id=>810004,p_page_id=>1,p_username=>'VERIFIER');
 session_id:=apex_application.g_instance;
 insert into hello_entries(entry_text) values('Hello') returning entry_id into h;
 insert into world_entries(entry_text) values('World') returning entry_id into w;
 update hello_config set default_entry_id=h where config_id=1;
 update world_config set default_entry_id=w where config_id=1;
 for i in 1..20 loop
  greeting:=lab_runtime.record_greeting;
  if greeting<>'Hello World' then raise_application_error(-20784,'Fixture greeting differs'); end if;
 end loop;
 commit;
 apex_session.delete_session(p_session_id=>session_id);
 dbms_output.put_line('PASS twenty initial-release qualification snapshots prepared through runtime API; browser verification follows.');
exception when others then rollback; raise;
end;
/
