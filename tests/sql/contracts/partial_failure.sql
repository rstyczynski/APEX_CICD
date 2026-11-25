declare l_sid number;l_code number:=0;l_count number;
begin
 apex_session.create_session(810603,1,'ALICE');l_sid:=apex_application.g_instance;
 apex_util.set_session_state('P1_COUNTRY','PL');
 insert into caller_markers values(1);
 begin e6_app.secure_greetings.submit_request('FAIL-AUDIT','PL','World');
 exception when others then l_code:=sqlcode; end;
 if l_code<>-20499 then raise_application_error(-20482,'Wrong injected error: '||l_code); end if;
 select count(*) into l_count from caller_markers where id=1;
 if l_count<>1 then raise_application_error(-20483,'Caller work was rolled back'); end if;
 rollback;
 apex_session.delete_session(l_sid);
 dbms_output.put_line('E6_PARTIAL_PASS: second-write error propagated, caller marker preserved until explicit rollback');
exception when others then
 rollback;
 if l_sid is not null then apex_session.delete_session(l_sid); end if;
 raise;
end;
/
