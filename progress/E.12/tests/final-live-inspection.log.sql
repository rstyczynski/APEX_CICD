whenever sqlerror exit failure rollback
whenever oserror exit failure rollback
set heading off feedback off pagesize 0 linesize 200
alter session set container=FREEPDB1;
select 'VERSION:'||version from E12_RUN_49496.component_version;
select 'SOURCE_HISTORY:'||id||':'||message||':'||nvl(language,'NULL') from E12_RUN_49496.history where id=0;
select 'TARGET_HISTORY:'||id||':'||message||':'||nvl(language,'NULL') from E12_RUN_49496.next_history where id=0;
select 'GREETING_DEFAULT:'||E12_RUN_49496.greet_language('Jan') from dual;
select 'GREETING_POLISH:'||E12_RUN_49496.greet_language('Jan','pl') from dual;
select 'SETTING:'||k||':'||v from E12_RUN_49496.settings;
select 'TARGET:'||id||':'||message from E12_RUN_49496.next_history where id in (1,3) order by id;
select 'DELETED_TARGET_ROWS:'||count(*) from E12_RUN_49496.next_history where id=2;
select 'HELLO_ROWS:'||count(*) from E12_RUN_49496.history where id between 1001 and 1120;
select 'WORLD_ROWS:'||count(*) from E12_RUN_49496.history where id between 2001 and 2120;
select 'JOURNAL:'||op||':'||count(*) from E12_RUN_49496.change_log where actor='E12_CONCURRENT' group by op order by op;
prompt FINAL_LIVE_INSPECTION_COMPLETE
exit
