-- Read-only field-level baseline for retained initial-release history and settings.
set sqlformat csv
select json_object(*) as history_row from greeting_history order by greeting_id;
select json_object(*) as hello_setting from hello_config order by config_id;
select json_object(*) as world_setting from world_config order by config_id;
