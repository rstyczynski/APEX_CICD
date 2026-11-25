lock table e12_app.history in share mode;
merge into e12_app.next_history t using e12_app.history s on(t.id=s.id)
when matched then update set t.message=s.message,t.language=s.language
when not matched then insert(id,message,language) values(s.id,s.message,s.language);
delete from e12_app.next_history t where not exists(select 1 from e12_app.history s where s.id=t.id);
declare n number; begin
select count(*) into n from ((select * from e12_app.history minus select * from e12_app.next_history) union all (select * from e12_app.next_history minus select * from e12_app.history));
if n<>0 then raise_application_error(-20003,'cutover mismatch'); end if;
dbms_output.put_line('CUTOVER_EQUAL');
end;
/
commit;
