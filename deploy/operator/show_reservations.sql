whenever oserror exit failure rollback
whenever sqlerror exit failure rollback
set sqlformat csv
select component,owner_name,task_id,base_revision,generation
from e1_reservations order by component;
