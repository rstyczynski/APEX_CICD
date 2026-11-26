update e12_app.callers set api=2,maintenance=0 where component='World';
insert into e12_app.migrations values('World','complete');
commit;
begin e12_app.request('World',2500);
commit; end;
/