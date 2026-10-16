prompt --application/pages/page_groups
begin
--   Manifest
--     PAGE GROUPS: 810002
--   Manifest End
wwv_flow_imp.component_begin (
 p_version_yyyy_mm_dd=>'2024.11.30'
,p_release=>'24.2.0'
,p_default_workspace_id=>3164667463725942
,p_default_application_id=>810001
,p_default_id_offset=>4766506890374761
,p_default_owner=>'E1_DEV_A'
);
wwv_flow_imp_page.create_page_group(
 p_id=>wwv_flow_imp.id(3775492943801313)
,p_group_name=>'Administration'
);
wwv_flow_imp.component_end;
end;
/
