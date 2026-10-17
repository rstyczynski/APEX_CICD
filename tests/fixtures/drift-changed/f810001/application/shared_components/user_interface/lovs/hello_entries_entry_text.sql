prompt --application/shared_components/user_interface/lovs/hello_entries_entry_text
begin
--   Manifest
--     HELLO_ENTRIES.ENTRY_TEXT
--   Manifest End
wwv_flow_imp.component_begin (
 p_version_yyyy_mm_dd=>'2024.11.30'
,p_release=>'24.2.0'
,p_default_workspace_id=>3164667463725942
,p_default_application_id=>810001
,p_default_id_offset=>4796272935437553
,p_default_owner=>'E1_DEV_A'
);
wwv_flow_imp_shared.create_list_of_values(
 p_id=>wwv_flow_imp.id(17747371016385)
,p_lov_name=>'HELLO_ENTRIES.ENTRY_TEXT'
,p_source_type=>'TABLE'
,p_location=>'LOCAL'
,p_query_table=>'HELLO_ENTRIES'
,p_return_column_name=>'ENTRY_ID'
,p_display_column_name=>'ENTRY_TEXT'
,p_default_sort_column_name=>'ENTRY_TEXT'
,p_default_sort_direction=>'ASC'
,p_version_scn=>3322208
);
wwv_flow_imp.component_end;
end;
/
