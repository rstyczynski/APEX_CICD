alter table hello_config
    add
        foreign key ( default_entry_id )
            references hello_entries ( entry_id )
        enable;


-- sqlcl_snapshot {"hash":"4ec1cc7f8c23b111de92e96fb425d78eb9709e2d","type":"REF_CONSTRAINT","name":"HELLO_CONFIG.HELLO_ENTRIES","schemaName":"E1_DEV_C","sxml":""}