-- Intentional release data, not a copy of authoring/runtime business rows.
merge into e2_components t using (
  select 'Foundation' component,'1.0.0' version from dual union all
  select 'Hello','1.0.0' from dual union all select 'World','1.0.0' from dual
) s on (t.component=s.component)
when not matched then insert(component,version) values(s.component,s.version);
merge into e2_settings t using (
  select 'HELLO' setting_key,'Hello' setting_value from dual union all
  select 'WORLD','World' from dual
) s on (t.setting_key=s.setting_key)
when not matched then insert(setting_key,setting_value) values(s.setting_key,s.setting_value);
commit;
