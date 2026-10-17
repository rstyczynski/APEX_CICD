prompt --application/pages/page_00110
begin
--   Manifest
--     PAGE: 00110
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
 p_id=>110
,p_name=>'Hello configuration'
,p_alias=>'HELLO-CONFIGURATION'
,p_step_title=>'Hello configuration'
,p_autocomplete_on_off=>'OFF'
,p_page_template_options=>'#DEFAULT#'
,p_protection_level=>'C'
,p_page_component_map=>'18'
);
wwv_flow_imp_page.create_page_plug(
 p_id=>wwv_flow_imp.id(24009089016393)
,p_plug_name=>'Hello configuration'
,p_region_template_options=>'#DEFAULT#:t-IRR-region--hideHeader js-addHiddenHeadingRoleDesc'
,p_plug_template=>2100526641005906379
,p_plug_display_sequence=>10
,p_query_type=>'TABLE'
,p_query_table=>'HELLO_CONFIG'
,p_include_rowid_column=>false
,p_plug_source_type=>'NATIVE_IR'
,p_prn_page_header=>'Hello configuration'
);
wwv_flow_imp_page.create_worksheet(
 p_id=>wwv_flow_imp.id(24106791016393)
,p_name=>'Hello configuration'
,p_max_row_count_message=>'The maximum row count for this report is #MAX_ROW_COUNT# rows.  Please apply a filter to reduce the number of records in your query.'
,p_no_data_found_message=>'No data found.'
,p_base_pk1=>'CONFIG_ID'
,p_pagination_type=>'ROWS_X_TO_Y'
,p_pagination_display_pos=>'BOTTOM_RIGHT'
,p_report_list_mode=>'TABS'
,p_lazy_loading=>false
,p_show_detail_link=>'C'
,p_show_notify=>'Y'
,p_download_formats=>'CSV:HTML:XLSX:PDF'
,p_enable_mail_download=>'Y'
,p_detail_link=>'f?p=&APP_ID.:111:&APP_SESSION.::&DEBUG.:RP:P111_CONFIG_ID:\#CONFIG_ID#\'
,p_detail_link_text=>'<span role="img" aria-label="Edit" class="fa fa-edit" title="Edit"></span>'
,p_owner=>'DEV_B'
,p_internal_uid=>4790613681391154
);
wwv_flow_imp_page.create_worksheet_column(
 p_id=>wwv_flow_imp.id(24759463016396)
,p_db_column_name=>'CONFIG_ID'
,p_display_order=>0
,p_is_primary_key=>'Y'
,p_column_identifier=>'A'
,p_column_label=>'Config ID'
,p_column_type=>'NUMBER'
,p_display_text_as=>'HIDDEN_ESCAPE_SC'
,p_heading_alignment=>'LEFT'
,p_tz_dependent=>'N'
,p_use_as_row_header=>'N'
);
wwv_flow_imp_page.create_worksheet_column(
 p_id=>wwv_flow_imp.id(25153906016399)
,p_db_column_name=>'PREFIX'
,p_display_order=>2
,p_column_identifier=>'B'
,p_column_label=>'Prefix'
,p_column_type=>'STRING'
,p_heading_alignment=>'LEFT'
,p_tz_dependent=>'N'
,p_use_as_row_header=>'N'
);
wwv_flow_imp_page.create_worksheet_column(
 p_id=>wwv_flow_imp.id(25578889016399)
,p_db_column_name=>'DEFAULT_ENTRY_ID'
,p_display_order=>3
,p_column_identifier=>'C'
,p_column_label=>'Default Entry'
,p_column_type=>'STRING'
,p_display_text_as=>'LOV_ESCAPE_SC'
,p_heading_alignment=>'LEFT'
,p_tz_dependent=>'N'
,p_rpt_named_lov=>wwv_flow_imp.id(17747371016385)
,p_use_as_row_header=>'N'
);
wwv_flow_imp_page.create_worksheet_rpt(
 p_id=>wwv_flow_imp.id(37252051104231)
,p_application_user=>'APXWS_DEFAULT'
,p_report_seq=>10
,p_report_alias=>'48336'
,p_status=>'PUBLIC'
,p_is_default=>'Y'
,p_report_columns=>'CONFIG_ID:PREFIX:DEFAULT_ENTRY_ID'
);
wwv_flow_imp_page.create_page_plug(
 p_id=>wwv_flow_imp.id(27619471016400)
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
wwv_flow_imp_page.create_page_button(
 p_id=>wwv_flow_imp.id(26069986016399)
,p_button_sequence=>10
,p_button_plug_id=>wwv_flow_imp.id(24009089016393)
,p_button_name=>'CREATE'
,p_button_action=>'REDIRECT_PAGE'
,p_button_template_options=>'#DEFAULT#'
,p_button_template_id=>4072362960822175091
,p_button_is_hot=>'Y'
,p_button_image_alt=>'Create'
,p_button_position=>'RIGHT_OF_IR_SEARCH_BAR'
,p_button_redirect_url=>'f?p=&APP_ID.:111:&APP_SESSION.::&DEBUG.:111::'
,p_button_condition_type=>'NEVER'
);
wwv_flow_imp_page.create_page_da_event(
 p_id=>wwv_flow_imp.id(26355807016399)
,p_name=>'Edit Report - Dialog Closed'
,p_event_sequence=>10
,p_triggering_element_type=>'REGION'
,p_triggering_region_id=>wwv_flow_imp.id(24009089016393)
,p_bind_type=>'bind'
,p_execution_type=>'IMMEDIATE'
,p_bind_event_type=>'apexafterclosedialog'
);
wwv_flow_imp_page.create_page_da_action(
 p_id=>wwv_flow_imp.id(26820815016399)
,p_event_id=>wwv_flow_imp.id(26355807016399)
,p_event_result=>'TRUE'
,p_action_sequence=>10
,p_execute_on_page_init=>'N'
,p_action=>'NATIVE_REFRESH'
,p_affected_elements_type=>'REGION'
,p_affected_region_id=>wwv_flow_imp.id(24009089016393)
);
wwv_flow_imp.component_end;
end;
/
