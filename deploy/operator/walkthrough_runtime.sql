-- Explicit CLI rehearsal fixture, after empty installation; never release seed.
set define on verify off serveroutput on
declare h number; w number; greeting varchar2(32767); sid number;
begin
 if user<>'&1' then raise_application_error(-20801,'Runtime verification identity mismatch'); end if;
 apex_util.set_workspace(user);
 apex_session.create_session(p_app_id=>to_number('&2'),p_page_id=>1,p_username=>'VERIFIER');
 sid:=apex_application.g_instance;
 select min(entry_id) into h from hello_entries where entry_text='Hello' and active='Y';
 if h is null then insert into hello_entries(entry_text) values('Hello') returning entry_id into h; end if;
 select min(entry_id) into w from world_entries where entry_text='World' and active='Y';
 if w is null then insert into world_entries(entry_text) values('World') returning entry_id into w; end if;
 update hello_config set default_entry_id=h where config_id=1 and default_entry_id is null;
 update world_config set default_entry_id=w where config_id=1 and default_entry_id is null;
 greeting:=lab_runtime.record_greeting;
 if greeting<>'Hello World' then raise_application_error(-20802,'Runtime greeting differs'); end if;
 commit;
 apex_session.delete_session(p_session_id=>sid);
 dbms_output.put_line('PASS CLI runtime verification: NEW Hello World snapshot. No browser acceptance claimed.');
exception when others then rollback; raise;
end;
/
