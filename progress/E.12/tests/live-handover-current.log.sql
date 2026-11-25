select version from e12_app.component_version;
select e12_app.foundation.greet('Jan'),e12_app.greet_language('Jan','pl') from dual;
select k||'='||v from e12_app.settings;
select id||':'||message from e12_app.next_history where id in (1,2,3) order by id;
select 'deleted-ID-2-count='||count(*) from e12_app.next_history where id=2;
select op||':'||count(*) from e12_app.change_log where actor='E12_CONCURRENT' group by op order by op;
