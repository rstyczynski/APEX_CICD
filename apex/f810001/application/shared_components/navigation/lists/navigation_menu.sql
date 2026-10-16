prompt --application/shared_components/navigation/lists/navigation_menu
begin
--   Manifest
--     LIST: Navigation Menu
--   Manifest End
wwv_flow_imp.component_begin (
 p_version_yyyy_mm_dd=>'2024.11.30'
,p_release=>'24.2.0'
,p_default_workspace_id=>3164667463725942
,p_default_application_id=>810001
,p_default_id_offset=>4796272935437553
,p_default_owner=>'E1_DEV_A'
);
wwv_flow_imp_shared.create_list(
 p_id=>wwv_flow_imp.id(3770389353801277)
,p_name=>'Navigation Menu'
,p_list_status=>'PUBLIC'
,p_version_scn=>3329889
);
wwv_flow_imp_shared.create_list_item(
 p_id=>wwv_flow_imp.id(3782159331801329)
,p_list_item_display_sequence=>10
,p_list_item_link_text=>'Home'
,p_list_item_link_target=>'f?p=&APP_ID.:1:&APP_SESSION.::&DEBUG.:::'
,p_list_item_icon=>'fa-home'
,p_list_item_current_type=>'TARGET_PAGE'
);
wwv_flow_imp_shared.create_list_item(
 p_id=>wwv_flow_imp.id(4570559250335274)
,p_list_item_display_sequence=>20
,p_list_item_link_text=>'Greeting history'
,p_list_item_link_target=>'f?p=&APP_ID.:10:&APP_SESSION.::&DEBUG.:::'
,p_list_item_icon=>'fa-table'
,p_list_item_current_type=>'COLON_DELIMITED_PAGE_LIST'
,p_list_item_current_for_pages=>'10'
);
wwv_flow_imp_shared.create_list_item(
 p_id=>wwv_flow_imp.id(10501949012121)
,p_list_item_display_sequence=>30
,p_list_item_link_text=>'Hello entries'
,p_list_item_link_target=>'f?p=&APP_ID.:100:&APP_SESSION.::&DEBUG.:::'
,p_list_item_icon=>'fa-table'
,p_list_item_current_type=>'COLON_DELIMITED_PAGE_LIST'
,p_list_item_current_for_pages=>'100,101'
);
wwv_flow_imp_shared.create_list_item(
 p_id=>wwv_flow_imp.id(23626740016392)
,p_list_item_display_sequence=>40
,p_list_item_link_text=>'Hello configuration'
,p_list_item_link_target=>'f?p=&APP_ID.:110:&APP_SESSION.::&DEBUG.:::'
,p_list_item_icon=>'fa-table'
,p_list_item_current_type=>'COLON_DELIMITED_PAGE_LIST'
,p_list_item_current_for_pages=>'110,111'
);
wwv_flow_imp_shared.create_list_item(
 p_id=>wwv_flow_imp.id(10879333008198)
,p_list_item_display_sequence=>50
,p_list_item_link_text=>'World entries'
,p_list_item_link_target=>'f?p=&APP_ID.:200:&APP_SESSION.::&DEBUG.:::'
,p_list_item_icon=>'fa-table'
,p_list_item_current_type=>'COLON_DELIMITED_PAGE_LIST'
,p_list_item_current_for_pages=>'200,201'
);
wwv_flow_imp_shared.create_list_item(
 p_id=>wwv_flow_imp.id(24217287016983)
,p_list_item_display_sequence=>60
,p_list_item_link_text=>'World configuration'
,p_list_item_link_target=>'f?p=&APP_ID.:210:&APP_SESSION.::&DEBUG.:::'
,p_list_item_icon=>'fa-table'
,p_list_item_current_type=>'COLON_DELIMITED_PAGE_LIST'
,p_list_item_current_for_pages=>'210,211'
);
wwv_flow_imp.component_end;
end;
/
