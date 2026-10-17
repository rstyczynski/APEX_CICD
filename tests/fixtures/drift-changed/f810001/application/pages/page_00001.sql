prompt --application/pages/page_00001
begin
--   Manifest
--     PAGE: 00001
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
 p_id=>1
,p_name=>'Home'
,p_alias=>'HOME'
,p_step_title=>'APEX Delivery Laboratory - direct change'
,p_allow_duplicate_submissions=>'N'
,p_welcome_text=>'<p>DIRECT CHANGE - deployment must stop</p>'
,p_autocomplete_on_off=>'OFF'
,p_page_template_options=>'#DEFAULT#'
,p_protection_level=>'C'
,p_page_component_map=>'13'
);
wwv_flow_imp_page.create_page_plug(
 p_id=>wwv_flow_imp.id(3783024278801331)
,p_plug_name=>'APEX Delivery Laboratory'
,p_region_template_options=>'#DEFAULT#'
,p_escape_on_http_output=>'Y'
,p_plug_template=>2674017834225413037
,p_plug_display_sequence=>10
,p_plug_display_point=>'REGION_POSITION_01'
,p_plug_query_num_rows=>15
,p_region_image=>'#APP_FILES#icons/app-icon-512.png'
,p_attributes=>wwv_flow_t_plugin_attributes(wwv_flow_t_varchar2(
  'expand_shortcuts', 'N',
  'output_as', 'HTML',
  'show_line_breaks', 'Y')).to_clob
);
wwv_flow_imp_page.create_page_button(
 p_id=>wwv_flow_imp.id(4564701405325001)
,p_button_sequence=>10
,p_button_plug_id=>wwv_flow_imp.id(3783024278801331)
,p_button_name=>'CREATE_GREETING'
,p_button_action=>'SUBMIT'
,p_button_template_options=>'#DEFAULT#'
,p_button_template_id=>4072362960822175091
,p_button_image_alt=>'Create greeting'
);
wwv_flow_imp_page.create_page_item(
 p_id=>wwv_flow_imp.id(30045675059848)
,p_name=>'P1_HELLO_CHOICE'
,p_item_sequence=>20
,p_item_plug_id=>wwv_flow_imp.id(3783024278801331)
,p_prompt=>'Hello'
,p_display_as=>'NATIVE_SELECT_LIST'
,p_lov=>'select entry_text d, entry_id r from hello_entries where active=''Y'' order by entry_text,entry_id'
,p_lov_display_null=>'YES'
,p_lov_null_text=>'Configured Hello default'
,p_cHeight=>1
,p_field_template=>1609121967514267634
,p_item_template_options=>'#DEFAULT#'
,p_lov_display_extra=>'YES'
,p_attributes=>wwv_flow_t_plugin_attributes(wwv_flow_t_varchar2(
  'page_action_on_selection', 'NONE')).to_clob
);
wwv_flow_imp_page.create_page_item(
 p_id=>wwv_flow_imp.id(30145981059849)
,p_name=>'P1_WORLD_CHOICE'
,p_item_sequence=>30
,p_item_plug_id=>wwv_flow_imp.id(3783024278801331)
,p_prompt=>'World'
,p_display_as=>'NATIVE_SELECT_LIST'
,p_lov=>'select entry_text d, entry_id r from world_entries where active=''Y'' order by entry_text,entry_id'
,p_lov_display_null=>'YES'
,p_lov_null_text=>'Configured World default'
,p_cHeight=>1
,p_field_template=>1609121967514267634
,p_item_template_options=>'#DEFAULT#'
,p_lov_display_extra=>'YES'
,p_attributes=>wwv_flow_t_plugin_attributes(wwv_flow_t_varchar2(
  'page_action_on_selection', 'NONE')).to_clob
);
wwv_flow_imp_page.create_page_process(
 p_id=>wwv_flow_imp.id(4564852750325002)
,p_process_sequence=>10
,p_process_point=>'ON_SUBMIT_BEFORE_COMPUTATION'
,p_process_type=>'NATIVE_PLSQL'
,p_process_name=>'Save greeting snapshot'
,p_process_sql_clob=>unistr('declare v varchar2(261 char); begin v:=lab_runtime.record_greeting(:P1_HELLO_CHOICE,:P1_WORLD_CHOICE); apex_application.g_print_success_message:=apex_escape.html(v)||'' \2014 saved to history.''; end;')
,p_process_clob_language=>'PLSQL'
,p_error_display_location=>'INLINE_IN_NOTIFICATION'
,p_process_when_button_id=>wwv_flow_imp.id(4564701405325001)
,p_internal_uid=>4564852750325002
);
wwv_flow_imp.component_end;
end;
/
