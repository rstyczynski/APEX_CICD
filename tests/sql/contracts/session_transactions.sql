declare
 l_sid number; l_code number; l_count number;
 procedure expect_rejection(p_country varchar2,p_code number) is
 begin
  l_code:=0;
  begin e6_app.secure_greetings.submit_request('SESSION-DENY',p_country,'World');
  exception when others then l_code:=sqlcode; end;
  if l_code<>p_code then raise_application_error(-20480,'Wrong country rejection: '||l_code); end if;
 end;
begin
 expect_rejection('PL',-20400);
 apex_session.create_session(810603,1,'ALICE');l_sid:=apex_application.g_instance;
 apex_util.set_session_state('P1_COUNTRY','PL');
 e6_app.secure_greetings.submit_request('ALLOWED-ROLLBACK','PL','World');
 expect_rejection('DE',-20401);
 apex_util.set_session_state('P1_COUNTRY','DE');
 expect_rejection('DE',-20402);
 rollback;
 apex_session.delete_session(l_sid);l_sid:=null;
 apex_session.create_session(810603,1,'BOB');l_sid:=apex_application.g_instance;
 apex_util.set_session_state('P1_COUNTRY','DE');
 e6_app.secure_greetings.submit_request('BOB-ALLOWED','DE','World');
 rollback;
 apex_session.delete_session(l_sid);l_sid:=null;
 -- This app's actual initialization code throws for this synthetic test identity.
 l_code:=0;
 begin apex_session.create_session(810603,1,'INIT_FAIL');
 exception when others then l_code:=sqlcode; dbms_output.put_line('INIT_FAILURE:'||sqlerrm); end;
 if l_code=0 then raise_application_error(-20481,'Initialization failure swallowed'); end if;
 if apex_application.g_instance is not null and apex_application.g_instance<>0 then
  apex_session.delete_session(apex_application.g_instance);
 end if;
 dbms_output.put_line('E6_SESSION_PASS: allowed ALICE/PL and BOB/DE; mismatch and denied writes rejected; initialization failure propagated; sessions deleted');
exception when others then
 rollback;
 if l_sid is not null then apex_session.delete_session(l_sid); end if;
 raise;
end;
/
