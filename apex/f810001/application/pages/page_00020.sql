prompt --application/pages/page_00020
begin
--   Manifest
--     PAGE: 00020
--   Manifest End
wwv_flow_imp.component_begin (
 p_version_yyyy_mm_dd=>'2024.11.30'
,p_release=>'24.2.0'
,p_default_workspace_id=>3164667463725942
,p_default_application_id=>810001
,p_default_id_offset=>4796272935437553
,p_default_owner=>'E1_DEV_A'
);
wwv_flow_imp_page.create_page(
 p_id=>20
,p_name=>'Installed components'
,p_alias=>'INSTALLED-COMPONENTS'
,p_step_title=>'Installed components'
,p_autocomplete_on_off=>'OFF'
,p_page_template_options=>'#DEFAULT#'
,p_protection_level=>'C'
);
wwv_flow_imp_page.create_page_plug(
 p_id=>wwv_flow_imp.id(195219108249667)
,p_plug_name=>'Breadcrumb'
,p_region_template_options=>'#DEFAULT#:t-BreadcrumbRegion--useBreadcrumbTitle'
,p_component_template_options=>'#DEFAULT#'
,p_plug_template=>2531463326621247859
,p_plug_display_sequence=>10
,p_plug_display_point=>'REGION_POSITION_01'
,p_menu_id=>wwv_flow_imp.id(3769886927801275)
,p_plug_source_type=>'NATIVE_BREADCRUMB'
,p_menu_template_id=>4072363345357175094
);
wwv_flow_imp_page.create_page_plug(
 p_id=>wwv_flow_imp.id(195925822249670)
,p_plug_name=>'Installed components'
,p_region_template_options=>'#DEFAULT#:t-IRR-region--hideHeader js-addHiddenHeadingRoleDesc'
,p_plug_template=>2100526641005906379
,p_plug_display_sequence=>10
,p_query_type=>'SQL'
,p_plug_source=>'select component, installed, version from lab_components order by component'
,p_plug_source_type=>'NATIVE_IR'
,p_prn_page_header=>'Installed components'
);
wwv_flow_imp_page.create_worksheet(
 p_id=>wwv_flow_imp.id(195957412249670)
,p_name=>'Installed components'
,p_max_row_count_message=>'The maximum row count for this report is #MAX_ROW_COUNT# rows.  Please apply a filter to reduce the number of records in your query.'
,p_no_data_found_message=>'No data found.'
,p_pagination_type=>'ROWS_X_TO_Y'
,p_pagination_display_pos=>'BOTTOM_RIGHT'
,p_report_list_mode=>'TABS'
,p_lazy_loading=>false
,p_show_detail_link=>'N'
,p_show_notify=>'Y'
,p_download_formats=>'CSV:HTML:XLSX:PDF'
,p_enable_mail_download=>'Y'
,p_owner=>'DEV_C'
,p_internal_uid=>4992230347687223
);
wwv_flow_imp_page.create_worksheet_column(
 p_id=>wwv_flow_imp.id(196677766249671)
,p_db_column_name=>'COMPONENT'
,p_display_order=>1
,p_column_identifier=>'A'
,p_column_label=>'Component'
,p_column_type=>'STRING'
,p_heading_alignment=>'LEFT'
,p_tz_dependent=>'N'
,p_use_as_row_header=>'N'
);
wwv_flow_imp_page.create_worksheet_column(
 p_id=>wwv_flow_imp.id(197107825249673)
,p_db_column_name=>'INSTALLED'
,p_display_order=>2
,p_column_identifier=>'B'
,p_column_label=>'Installed'
,p_column_type=>'NUMBER'
,p_heading_alignment=>'RIGHT'
,p_column_alignment=>'RIGHT'
,p_tz_dependent=>'N'
,p_use_as_row_header=>'N'
);
wwv_flow_imp_page.create_worksheet_column(
 p_id=>wwv_flow_imp.id(197505551249673)
,p_db_column_name=>'VERSION'
,p_display_order=>3
,p_column_identifier=>'C'
,p_column_label=>'Version'
,p_column_type=>'STRING'
,p_heading_alignment=>'LEFT'
,p_tz_dependent=>'N'
,p_use_as_row_header=>'N'
);
wwv_flow_imp.component_end;
end;
/
