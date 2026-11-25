alter table world_config
    add
        foreign key ( default_entry_id )
            references world_entries ( entry_id )
        enable;


-- sqlcl_snapshot {"hash":"8eb98b80d3ca26512d0f77899fd5232b8b646330","type":"REF_CONSTRAINT","name":"WORLD_CONFIG.WORLD_ENTRIES","schemaName":"E1_DEV_C","sxml":""}