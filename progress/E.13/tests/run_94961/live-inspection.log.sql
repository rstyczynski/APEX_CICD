select id,message from e12_app.history where id in (0,1000,2000,3000,3001,4001,4002) order by id;
select k,v from e12_app.settings;
select component,api from e12_app.callers order by component;
select legacy_enabled from e12_app.lifecycle;
select count(*) from e12_app.history;
select count(*) from e12_app.details;
