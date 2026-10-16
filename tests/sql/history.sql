set serveroutput on
declare h number; w number; first_id number; before_snapshot clob; after_snapshot clob; greeting varchar2(32767);
begin
  update lab_state set state='ready' where state_key='Application';
  insert into hello_entries(entry_text) values ('Hello') returning entry_id into h;
  insert into world_entries(entry_text) values ('World') returning entry_id into w;
  update hello_config set default_entry_id=h,prefix=null where config_id=1;
  update world_config set default_entry_id=w,prefix=null where config_id=1;
  greeting:=lab_runtime.record_greeting;
  select max(greeting_id) into first_id from greeting_history;
  select json_object(* returning clob) into before_snapshot from greeting_history where greeting_id=first_id;
  update hello_config set prefix='Welcome ' where config_id=1;
  update world_entries set entry_text='Earth' where entry_id=w;
  greeting:=lab_runtime.record_greeting;
  if greeting<>'Welcome Hello Earth' then raise_application_error(-20510,'Changed configuration was not applied'); end if;
  select json_object(* returning clob) into after_snapshot from greeting_history where greeting_id=first_id;
  if dbms_lob.compare(before_snapshot,after_snapshot)<>0 then raise_application_error(-20511,'Prior snapshot changed'); end if;
  begin
    update greeting_history set greeting_text='tampered' where greeting_id=first_id;
    raise_application_error(-20512,'History edit allowed');
  exception when others then if sqlcode<>-20305 then raise; end if; end;
  begin
    delete from greeting_history where greeting_id=first_id;
    raise_application_error(-20513,'History delete allowed');
  exception when others then if sqlcode<>-20305 then raise; end if; end;
  rollback;
  dbms_output.put_line('PASS UT-2: changed settings affect new greetings; all original snapshot fields preserved; update/delete denied. Fixtures rolled back.');
exception when others then rollback; raise;
end;
/
