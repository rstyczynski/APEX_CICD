create or replace function e1_recovery_observation return varchar2 authid current_user as
  result varchar2(4000); migrations varchar2(2000);
begin
  -- Scope is every index on the experiment's history table, including unexpected additions.
  select listagg(i.index_name||':'||i.uniqueness||':'||i.status||':'||o.object_id||':'||c.column_name||':'||c.column_position,'|')
    within group(order by i.index_name,c.column_position) into result
    from user_indexes i join user_ind_columns c on c.index_name=i.index_name
    join user_objects o on o.object_name=i.index_name and o.object_type='INDEX'
    where i.table_name='GREETING_HISTORY';
  select listagg(id||':'||author||':'||md5sum||':'||exectype,'|') within group(order by orderexecuted) into migrations from databasechangelog;
  return result||'|MIGRATIONS|'||migrations;
end;
/
