whenever oserror exit failure rollback
whenever sqlerror exit failure rollback
set sqlformat csv
select workspace,application_id,application_name,alias,version,availability_status
from apex_applications order by application_id;
