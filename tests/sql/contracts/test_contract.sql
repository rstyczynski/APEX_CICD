create or replace package test_contract as
 --%suite(Stable greeting consumers)
 --%suitepath(contracts)

 --%test(Existing named call preserves its result)
 procedure existing_consumer;
 --%test(Deprecated consumer remains callable)
 procedure legacy_consumer;
 --%test(Invalid input preserves its documented error)
 procedure invalid_input;
end;
/
create or replace package body test_contract as
 procedure existing_consumer is
 begin
  ut.expect(e6_app.greeting_contract.render(p_text=>'World')).to_equal('Hello World');
 end;
 procedure legacy_consumer is
 begin
  ut.expect(e6_app.greeting_contract.hello(p_name=>'World')).to_equal('Hello World');
 end;
 procedure invalid_input is
  l_text varchar2(200);l_code number:=0;
 begin
  begin l_text:=e6_app.greeting_contract.render('   ');
  exception when others then l_code:=sqlcode;
  end;
  ut.expect(l_code).to_equal(-20410);
 end;
end;
/
