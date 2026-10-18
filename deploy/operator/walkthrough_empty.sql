set serveroutput on
declare n number;
begin
 select count(*) into n from apex_applications where application_id between 810001 and 810005;
 if n<>0 then raise_application_error(-20800,'Fresh walkthrough requires absent applications'); end if;
 select count(*) into n from dba_tables where owner in ('E1_DEV_A','E1_DEV_B','E1_DEV_C','E1_INTEGRATION','E1_UAT')
  and table_name<>'E1_PRIVATE_PROBE';
 if n<>0 then raise_application_error(-20804,'Business objects survive in fresh areas'); end if;
 select (select count(*) from E1_CTRL.e1_control_events)+(select count(*) from E1_CTRL.e1_release_attempts) into n from dual;
 if n<>0 then raise_application_error(-20805,'Previous control events/attempts survive'); end if;
 select count(*) into n from E1_CTRL.e1_release_targets where epoch<>0 or phase<>'new' or owner_name is not null;
 if n<>0 then raise_application_error(-20806,'Fresh release targets required'); end if;
 dbms_output.put_line('PASS fresh authority: no old task/release events; targets new at epoch zero.');
 dbms_output.put_line('PASS empty inventory: applications 810001–810005 and all business/history tables absent.');
end;
/
