-- New literal qualification fixtures, not exported author/UAT business snapshots.
-- Apply only after reconstructing the initial archive into empty integration.
set serveroutput on
declare
  l_count number;
  l_text varchar2(261);
begin
  if user<>'E1_INTEGRATION' then raise_application_error(-20870,'Wrong fixture target'); end if;
  select count(*) into l_count from lab_components where installed=1 and version='1.0.0';
  if l_count<>3 then raise_application_error(-20871,'Fixture requires complete initial 1.0.0'); end if;
  select count(*) into l_count from greeting_history;
  if l_count<>0 then raise_application_error(-20872,'Fixture refuses existing history; inspect'); end if;
  update hello_config set prefix='QUAL:' where config_id=1 and prefix is null;
  if sql%rowcount<>1 then raise_application_error(-20873,'Fixture refuses an existing prefix'); end if;
  apex_util.set_workspace('E1_INTEGRATION');
  apex_session.create_session(p_app_id=>810004,p_page_id=>1,p_username=>'VERIFIER');
  l_text:=lab_runtime.record_greeting;
  if l_text<>'QUAL:Hello World' then raise_application_error(-20874,'Qualification greeting mismatch'); end if;
  commit;
  apex_session.delete_session;
  dbms_output.put_line('PASS new qualification fixture: QUAL: prefix and retained QUAL:Hello World greeting');
end;
/
select greeting_id,greeting_text,hello_prefix,world_prefix,created_at,actor
 from greeting_history order by greeting_id;
select config_id,prefix,default_entry_id from hello_config;
