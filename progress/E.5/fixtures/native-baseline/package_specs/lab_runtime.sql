create or replace package lab_runtime authid definer as
    procedure assert_ready;

    function record_greeting (
        p_hello_id number default null,
        p_world_id number default null
    ) return varchar2;

end;
/


-- sqlcl_snapshot {"hash":"20ad4f35d79d7517021e6e2796fb8dae83b925a7","type":"PACKAGE_SPEC","name":"LAB_RUNTIME","schemaName":"E1_DEV_C","sxml":""}