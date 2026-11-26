begin begin e12_app.request('World',9999); raise_application_error(-20203,'maintenance bypass'); exception when others then if sqlcode<>-20201 then raise; end if; end; end;
/