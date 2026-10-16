prompt --application/shared_components/navigation/breadcrumbs/breadcrumb
begin
--   Manifest
--     MENU: Breadcrumb
--   Manifest End
wwv_flow_imp.component_begin (
 p_version_yyyy_mm_dd=>'2024.11.30'
,p_release=>'24.2.0'
,p_default_workspace_id=>3164667463725942
,p_default_application_id=>810001
,p_default_id_offset=>4796272935437553
,p_default_owner=>'E1_DEV_A'
);
wwv_flow_imp_shared.create_menu(
 p_id=>wwv_flow_imp.id(3769886927801275)
,p_name=>'Breadcrumb'
);
wwv_flow_imp_shared.create_menu_option(
 p_id=>wwv_flow_imp.id(14546689012130)
,p_short_name=>'Hello entries'
,p_link=>'f?p=&APP_ID.:100:&APP_SESSION.::&DEBUG.:::'
,p_page_id=>100
);
wwv_flow_imp_shared.create_menu_option(
 p_id=>wwv_flow_imp.id(14806335008208)
,p_short_name=>'World entries'
,p_link=>'f?p=&APP_ID.:200:&APP_SESSION.::&DEBUG.:::'
,p_page_id=>200
);
wwv_flow_imp_shared.create_menu_option(
 p_id=>wwv_flow_imp.id(27538619016400)
,p_short_name=>'Hello configuration'
,p_link=>'f?p=&APP_ID.:110:&APP_SESSION.::&DEBUG.:::'
,p_page_id=>110
);
wwv_flow_imp_shared.create_menu_option(
 p_id=>wwv_flow_imp.id(28135470016989)
,p_short_name=>'World configuration'
,p_link=>'f?p=&APP_ID.:210:&APP_SESSION.::&DEBUG.:::'
,p_page_id=>210
);
wwv_flow_imp_shared.create_menu_option(
 p_id=>wwv_flow_imp.id(3770014920801276)
,p_short_name=>'Home'
,p_link=>'f?p=&APP_ID.:1:&APP_SESSION.::&DEBUG.:::'
,p_page_id=>1
);
wwv_flow_imp_shared.create_menu_option(
 p_id=>wwv_flow_imp.id(4571488758335279)
,p_short_name=>'Greeting history'
,p_link=>'f?p=&APP_ID.:10:&APP_SESSION.::&DEBUG.:::'
,p_page_id=>10
);
wwv_flow_imp.component_end;
end;
/
