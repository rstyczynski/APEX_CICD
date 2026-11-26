create or replace package test_hello_entry_api as
  --%suite(Hello entry API)
  --%suitepath(backend)

  --%test(Trims valid text)
  procedure trims_text;
  --%test(Rejects blank input without writes)
  procedure rejects_blank;
  --%test(Accepts exactly one hundred characters)
  procedure accepts_limit;
  --%test(Rejects one hundred and one characters without writes)
  procedure rejects_long;
  --%test(Rejects invalid active flag without writes)
  procedure rejects_active;
end;
/
create or replace package body test_hello_entry_api as
  procedure trims_text is
    l_id number; l_text hello_entries.entry_text%type;
    l_fixed_time constant timestamp with time zone := to_timestamp_tz(
      '2026-11-25 12:00:00 +00:00','YYYY-MM-DD HH24:MI:SS TZH:TZM');
  begin
    hello_entry_api.create_entry('  E5 fixture '||to_char(l_fixed_time,'YYYY-MM-DD')||'  ', 'Y', l_id);
    select entry_text into l_text from hello_entries where entry_id=l_id;
    ut.expect(l_text).to_equal('E5 fixture 2026-11-25');
  end;
  procedure assert_rejected(p_text varchar2, p_active varchar2, p_code number) is
    l_id number; l_before number; l_after number; l_code number := 0;
  begin
    select count(*) into l_before from hello_entries;
    begin
      hello_entry_api.create_entry(p_text, p_active, l_id);
    exception when others then l_code := sqlcode;
    end;
    ut.expect(l_code).to_equal(p_code);
    select count(*) into l_after from hello_entries;
    ut.expect(l_after).to_equal(l_before);
  end;
  procedure rejects_blank is
  begin
    assert_rejected(null,'Y',-20320);
    assert_rejected('   ','Y',-20320);
  end;
  procedure accepts_limit is
    l_id number; l_text varchar2(100);
  begin
    hello_entry_api.create_entry(rpad('x',100,'x'),'N',l_id);
    select entry_text into l_text from hello_entries where entry_id=l_id;
    ut.expect(length(l_text)).to_equal(100);
  end;
  procedure rejects_long is
  begin
    assert_rejected(rpad('x',101,'x'),'Y',-20320);
  end;
  procedure rejects_active is
  begin
    assert_rejected('E5 invalid flag','X',-20321);
    assert_rejected('E5 null flag',null,-20321);
  end;
end;
/
