"""Replay only the isolated app's native page metadata, preserving business rows."""
import os,sys,subprocess,json
from backend_admin import sql,ROOT
variant=sys.argv[1] if len(sys.argv)==2 else ''
if variant not in ('baseline','api'):raise SystemExit('Usage: backend_page_variant.py baseline|api')
config=json.loads((ROOT/'examples/testable-backend/.dbtools/project.config.json').read_text())
env=os.environ.copy();env['JAVA_HOME']=str(ROOT/'.local-apex/tools/jdk-21.0.12.1+1/Contents/Home')
version=subprocess.check_output([str(ROOT/'.local-apex/tools/sqlcl-25.4.1.022.0618/sqlcl/bin/sql'),'-version'],env=env,text=True)
assert config['sqlcl']['version']=='25.4.1.0' and '25.4.1.022.0618' in version
source=(ROOT/('progress/E.5/fixtures/native-baseline/f810003.sql' if variant=='baseline' else 'examples/testable-backend/apex/f810503.sql')).read_text()
body="""begin
 apex_application_install.set_workspace('E5_PAGE');
 apex_application_install.set_application_id(810503);
 apex_application_install.generate_offset;
 apex_application_install.set_schema('E5_PAGE');
 apex_application_install.set_application_alias('E5-BACKEND');
end;
/
"""+source
sql(body,'page-variant-'+variant+'.log')
print('Imported '+variant+' metadata into isolated app 810503; reload and sign in. Business tables were not reset.')
