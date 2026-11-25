select E12_RUN_89176.greet_language('Jan') as legacy,E12_RUN_89176.greet_language('Jan','pl') as polish from dual;
select id,message,language from E12_RUN_89176.history where id<=3 order by id;
select 'deleted ID 2 count='||count(*) from E12_RUN_89176.history where id=2;
select k,v from E12_RUN_89176.settings;
select 'Hello accepted='||count(*) from E12_RUN_89176.history where id between 1001 and 1120;
select 'World accepted='||count(*) from E12_RUN_89176.history where id between 2001 and 2120;
select op,count(*) from E12_RUN_89176.change_log where actor='E12_CONCURRENT' group by op order by op;
