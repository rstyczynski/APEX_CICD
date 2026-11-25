declare n number; begin select count(*) into n from e12_app.fixture_owner where marker='APEX_CICD_E12'; if n<>1 then raise_application_error(-20017,'Wrong fixture'); end if; end;
/
select h.id||':'||h.message||':source_language='||nvl(h.language,'NULL')||':target='||t.message||':target_language='||nvl(t.language,'NULL') from e12_app.history h join e12_app.next_history t on t.id=h.id where h.id=0;
select version from e12_app.component_version;
select k||'='||v from e12_app.settings;
