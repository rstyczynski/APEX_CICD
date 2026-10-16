prompt --application/pages/page_00010
begin
--   Manifest
--     PAGE: 00010
--   Manifest End
wwv_flow_imp.component_begin (
 p_version_yyyy_mm_dd=>'2024.11.30'
,p_release=>'24.2.0'
,p_default_workspace_id=>3164667463725942
,p_default_application_id=>810001
,p_default_id_offset=>0
,p_default_owner=>'E1_DEV_A'
);
wwv_flow_imp_page.create_page(
 p_id=>10
,p_name=>'Greeting history'
,p_alias=>'GREETING-HISTORY'
,p_step_title=>'Greeting history'
,p_autocomplete_on_off=>'OFF'
,p_page_template_options=>'#DEFAULT#'
,p_protection_level=>'C'
);
wwv_flow_imp_page.create_page_plug(
 p_id=>wwv_flow_imp.id(4570963224335277)
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
 p_id=>wwv_flow_imp.id(4571620989335279)
,p_plug_name=>'Greeting history'
,p_region_template_options=>'#DEFAULT#:t-IRR-region--hideHeader js-addHiddenHeadingRoleDesc'
,p_plug_template=>2100526641005906379
,p_plug_display_sequence=>10
,p_query_type=>'SQL'
,p_plug_source=>'select greeting_id, greeting_text, hello_text, world_text, hello_prefix, world_prefix, created_at, actor from greeting_history order by created_at desc, greeting_id desc'
,p_plug_source_type=>'NATIVE_IR'
,p_prn_page_header=>'Greeting history'
);
wwv_flow_imp_page.create_worksheet(
 p_id=>wwv_flow_imp.id(4571742847335279)
,p_name=>'Greeting history'
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
,p_owner=>'DEV_A'
,p_internal_uid=>4571742847335279
);
wwv_flow_imp_page.create_worksheet_column(
 p_id=>wwv_flow_imp.id(4572475498335281)
,p_db_column_name=>'GREETING_ID'
,p_display_order=>1
,p_column_identifier=>'A'
,p_column_label=>'Greeting Id'
,p_column_type=>'NUMBER'
,p_heading_alignment=>'RIGHT'
,p_column_alignment=>'RIGHT'
,p_tz_dependent=>'N'
,p_use_as_row_header=>'N'
);
wwv_flow_imp_page.create_worksheet_column(
 p_id=>wwv_flow_imp.id(4572820386335284)
,p_db_column_name=>'GREETING_TEXT'
,p_display_order=>2
,p_column_identifier=>'B'
,p_column_label=>'Greeting Text'
,p_column_type=>'STRING'
,p_heading_alignment=>'LEFT'
,p_tz_dependent=>'N'
,p_use_as_row_header=>'N'
);
wwv_flow_imp_page.create_worksheet_column(
 p_id=>wwv_flow_imp.id(4573297503335284)
,p_db_column_name=>'HELLO_TEXT'
,p_display_order=>3
,p_column_identifier=>'C'
,p_column_label=>'Hello Text'
,p_column_type=>'STRING'
,p_heading_alignment=>'LEFT'
,p_tz_dependent=>'N'
,p_use_as_row_header=>'N'
);
wwv_flow_imp_page.create_worksheet_column(
 p_id=>wwv_flow_imp.id(4573693027335284)
,p_db_column_name=>'WORLD_TEXT'
,p_display_order=>4
,p_column_identifier=>'D'
,p_column_label=>'World Text'
,p_column_type=>'STRING'
,p_heading_alignment=>'LEFT'
,p_tz_dependent=>'N'
,p_use_as_row_header=>'N'
);
wwv_flow_imp_page.create_worksheet_column(
 p_id=>wwv_flow_imp.id(4574034584335285)
,p_db_column_name=>'HELLO_PREFIX'
,p_display_order=>5
,p_column_identifier=>'E'
,p_column_label=>'Hello Prefix'
,p_column_type=>'STRING'
,p_heading_alignment=>'LEFT'
,p_tz_dependent=>'N'
,p_use_as_row_header=>'N'
);
wwv_flow_imp_page.create_worksheet_column(
 p_id=>wwv_flow_imp.id(4574433184335285)
,p_db_column_name=>'WORLD_PREFIX'
,p_display_order=>6
,p_column_identifier=>'F'
,p_column_label=>'World Prefix'
,p_column_type=>'STRING'
,p_heading_alignment=>'LEFT'
,p_tz_dependent=>'N'
,p_use_as_row_header=>'N'
);
wwv_flow_imp_page.create_worksheet_column(
 p_id=>wwv_flow_imp.id(4574877415335285)
,p_db_column_name=>'CREATED_AT'
,p_display_order=>7
,p_column_identifier=>'G'
,p_column_label=>'Created At'
,p_column_type=>'DATE'
,p_heading_alignment=>'LEFT'
,p_tz_dependent=>'N'
,p_use_as_row_header=>'N'
);
wwv_flow_imp_page.create_worksheet_column(
 p_id=>wwv_flow_imp.id(4575303059335285)
,p_db_column_name=>'ACTOR'
,p_display_order=>8
,p_column_identifier=>'H'
,p_column_label=>'Actor'
,p_column_type=>'STRING'
,p_heading_alignment=>'LEFT'
,p_tz_dependent=>'N'
,p_use_as_row_header=>'N'
);
wwv_flow_imp.component_end;
end;
/
