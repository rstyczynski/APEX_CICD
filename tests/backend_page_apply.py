"""Apply the reviewed page-101 adapter to isolated app 810503 only."""
from pathlib import Path
import re,os,subprocess
from backend_admin import sql,ROOT
# Verify the source project's pinned release and exact qualified executable first.
import json
metadata=json.loads((ROOT/'examples/testable-backend/.dbtools/project.config.json').read_text())
env=os.environ.copy();env['JAVA_HOME']=str(ROOT/'.local-apex/tools/jdk-21.0.12.1+1/Contents/Home')
exe=ROOT/'.local-apex/tools/sqlcl-25.4.1.022.0618/sqlcl/bin/sql'
r=subprocess.run([str(exe),'-version'],env=env,text=True,capture_output=True,check=True)
assert metadata['sqlcl']['version']=='25.4.1.0' and '25.4.1.022.0618' in r.stdout
(ROOT/'progress/E.5/tests/sqlcl-qualified.log').write_text(r.stdout+r.stderr)
source=(ROOT/'progress/E.5/fixtures/native-baseline/f810003.sql').read_text()
pattern=r"wwv_flow_imp_page.create_page_process\(\n p_id=>wwv_flow_imp.id\(3280224224095888\).*?\n\);"
m=re.search(pattern,source,re.S);assert m and "Process form Hello entry" in m.group()
original=m.group();replacement=original.replace(",p_internal_uid=>",",p_process_when=>'SAVE,DELETE'\n,p_process_when_type=>'REQUEST_IN_CONDITION'\n,p_internal_uid=>")
replacement+="""
wwv_flow_imp_page.create_page_validation(
 p_id=>wwv_flow_imp.id(999000010)
,p_validation_name=>'Hello entry API validation'
,p_validation_sequence=>10
,p_validation=>'return hello_entry_api.validation_error(:P101_ENTRY_TEXT);'
,p_validation_type=>'FUNC_BODY_RETURNING_ERR_TEXT'
,p_validation_condition=>'CREATE'
,p_validation_condition_type=>'REQUEST_EQUALS_CONDITION'
,p_associated_item=>wwv_flow_imp.id(3275114195095882)
,p_error_display_location=>'INLINE_WITH_FIELD_AND_NOTIFICATION'
);
wwv_flow_imp_page.create_page_process(
 p_id=>wwv_flow_imp.id(999000011)
,p_process_sequence=>20
,p_process_point=>'AFTER_SUBMIT'
,p_process_type=>'NATIVE_PLSQL'
,p_process_name=>'Create Hello entry through API'
,p_process_sql_clob=>'begin hello_entry_api.create_entry(:P101_ENTRY_TEXT,:P101_ACTIVE,:P101_ENTRY_ID); end;'
,p_process_clob_language=>'PLSQL'
,p_process_when=>'CREATE'
,p_process_when_type=>'REQUEST_IN_CONDITION'
,p_error_display_location=>'INLINE_IN_NOTIFICATION'
);
"""
source=source[:m.start()]+replacement+source[m.end():]
# Retain native required-field behavior for SAVE and avoid duplicate blank errors:
source=source.replace("p_validation_condition=>'CREATE'","p_validation_condition=>':REQUEST = ''CREATE'' and :P101_ENTRY_TEXT is not null'").replace("p_validation_condition_type=>'REQUEST_EQUALS_CONDITION'","p_validation_condition_type=>'PLSQL_EXPRESSION'")
# Store the native importable prototype source, without a stale SQLcl snapshot receipt.
source=re.sub(r'(?m)^-- sqlcl_snapshot .*$', '',source)
out=ROOT/'.local-apex/e5/prepared-page.sql';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(source)
body="alter session set current_schema=E5_PAGE;\n"+(ROOT/'examples/testable-backend/sql/hello_entry_api.sql').read_text()+"\nalter session set current_schema=SYS;\n"
body+="""begin
 apex_application_install.set_workspace('E5_PAGE');
 apex_application_install.set_application_id(810503);
 apex_application_install.generate_offset;
 apex_application_install.set_schema('E5_PAGE');
 apex_application_install.set_application_alias('E5-BACKEND');
end;
/
"""+source
print(sql(body,'page-api-install.log')[-300:])
