whenever oserror exit failure rollback
whenever sqlerror exit failure rollback
set sqlformat csv
select component,installed,version from lab_components order by component;
select state_key,parent_key,state,reason from lab_state order by state_key;
select count(*) as saved_greetings from greeting_history;
