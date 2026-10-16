set serveroutput on
declare
  h number; w number; greeting varchar2(32767); n number;
begin
  update lab_state set state='ready' where state_key='Application';
  insert into hello_entries(entry_text) values ('  Hello  ') returning entry_id into h;
  insert into world_entries(entry_text) values ('World') returning entry_id into w;
  update hello_config set default_entry_id=h,prefix=null where config_id=1;
  update world_config set default_entry_id=w,prefix=null where config_id=1;
  greeting:=lab_runtime.record_greeting;
  if greeting<>'Hello World' then raise_application_error(-20500,'Default greeting differs'); end if;
  update hello_entries set entry_text='Cześć' where entry_id=h;
  update world_entries set entry_text='世界' where entry_id=w;
  update hello_config set prefix='[' where config_id=1;
  update world_config set prefix=']' where config_id=1;
  greeting:=lab_runtime.record_greeting(h,w);
  if greeting<>'[Cześć ]世界' then raise_application_error(-20501,'Unicode/prefix composition differs'); end if;
  begin
    update hello_entries set active='N' where entry_id=h;
    raise_application_error(-20502,'Default deactivation was allowed');
  exception when others then if sqlcode<>-20310 then raise; end if; end;
  select count(*) into n from greeting_history;
  begin
    greeting:=lab_runtime.record_greeting(-1,w);
    raise_application_error(-20503,'Unknown entry accepted');
  exception when others then if sqlcode<>-20304 then raise; end if; end;
  declare after_count number; begin
    select count(*) into after_count from greeting_history;
    if after_count<>n then raise_application_error(-20504,'Rejected selection inserted history'); end if;
  end;
  update hello_entries set entry_text=rpad('H',100,'H') where entry_id=h;
  update world_entries set entry_text=rpad('W',100,'W') where entry_id=w;
  update hello_config set prefix=rpad('a',30,'a') where config_id=1;
  update world_config set prefix=rpad('b',30,'b') where config_id=1;
  greeting:=lab_runtime.record_greeting;
  if length(greeting)<>261 then raise_application_error(-20505,'Boundary greeting length differs'); end if;
  begin
    insert into hello_entries(entry_text) values ('   ');
    raise_application_error(-20506,'Blank entry accepted');
  exception when others then if sqlcode not in (-1400,-2290) then raise; end if; end;
  begin
    insert into world_entries(entry_text) values (rpad('X',101,'X'));
    raise_application_error(-20507,'Oversize entry accepted');
  exception when others then if sqlcode<>-12899 then raise; end if; end;
  rollback;
  dbms_output.put_line('PASS UT-1: defaults, trim, Unicode, prefixes, explicit selections, invalid/default deactivation rejection and 261-character boundary. Fixtures rolled back.');
exception when others then rollback; raise;
end;
/
