begin apex_util.set_security_group_id(apex_util.find_security_group_id('E5_PAGE')); end;
/
declare
 n number; l_before number; l_after number; l_id number; l_code number:=0;
begin
 select count(*) into n from apex_application_page_val
 where application_id=810503 and page_id=101
 and validation_name='Hello entry API validation'
 and associated_item='P101_ENTRY_TEXT';
 if n<>1 then raise_application_error(-20330,'Item-specific API validation mapping missing'); end if;
 select count(*) into n from apex_application_page_proc
 where application_id=810503 and page_id=101
 and process_name='Create Hello entry through API'
 and condition_expression1='CREATE';
 if n<>1 then raise_application_error(-20331,'CREATE API process missing'); end if;
 select count(*) into n from apex_application_page_proc
 where application_id=810503 and page_id=101
 and process_name='Process form Hello entry'
 and condition_expression1='SAVE,DELETE';
 if n<>1 then raise_application_error(-20332,'Native DML not restricted to SAVE/DELETE'); end if;
 select count(*) into l_before from e5_page.hello_entries;
 begin e5_page.hello_entry_api.create_entry('   ','Y',l_id);
 exception when others then l_code:=sqlcode; end;
 if l_code<>-20320 then raise_application_error(-20333,'Wrong invalid-input rejection'); end if;
 select count(*) into l_after from e5_page.hello_entries;
 if l_before<>l_after then raise_application_error(-20334,'Invalid input changed rows'); end if;
 select count(*) into n from e5_page.hello_entries
 where (entry_text='E5 before' or entry_text='E5 after') and active='Y';
 if n<>2 then raise_application_error(-20335,'Before/after browser fixtures missing'); end if;
 select count(*) into n from dba_triggers
 where owner='E5_PAGE' and trigger_name='HELLO_ENTRIES_GUARD' and status='ENABLED';
 if n<>1 then raise_application_error(-20336,'Existing readiness trigger disabled'); end if;
 dbms_output.put_line('E5_PAGE_PASS: mapping, request boundaries, direct rejection, browser fixtures and enabled trigger');
end;
/
rollback;
