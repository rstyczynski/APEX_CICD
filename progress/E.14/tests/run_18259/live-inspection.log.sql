select component||': API='||api||', maintenance='||maintenance from e12_app.callers order by component;
select 'history='||count(*) from e12_app.history;
select 'details='||count(*) from e12_app.details;
select 'baseline='||message from e12_app.history where id=0;
select k||'='||v from e12_app.settings;