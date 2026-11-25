begin dbms_session.set_identifier('E12_CONCURRENT'); end;
/
insert into e12_app.history(id,message,language) values(3,'concurrent insert','pl');
update e12_app.history set message='newer accepted' where id=1;
delete from e12_app.history where id=2;
commit;
