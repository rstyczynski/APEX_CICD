-- Compatible metadata declaration and additive release setting.
update e2_components set version='1.0.1' where component='Hello';
merge into e2_settings t using (
  select 'LANGUAGE' setting_key,'en' setting_value from dual
) s on (t.setting_key=s.setting_key)
when not matched then insert(setting_key,setting_value) values(s.setting_key,s.setting_value);
commit;
