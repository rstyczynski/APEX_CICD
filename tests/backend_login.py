"""Set the existing isolated VERIFIER password through native APEX API."""
import getpass,sys
from backend_admin import sql
if sys.argv[1:]==['--password-stdin']:
 password=sys.stdin.readline().rstrip('\r\n')
elif not sys.argv[1:]:
 password=getpass.getpass('New password for E5_PAGE / VERIFIER: ')
else:raise SystemExit('Usage: backend_login.py [--password-stdin]')
if len(password)<16 or '\n' in password or '\r' in password:raise SystemExit('Use at least 16 characters and no line breaks.')
escaped=password.replace("'","''")
body="""begin
 apex_util.set_security_group_id(apex_util.find_security_group_id('E5_PAGE'));
 apex_util.edit_user(
   p_user_id=>apex_util.get_user_id('VERIFIER'),
   p_user_name=>'VERIFIER',
   p_web_password=>'"""+escaped+"""',
   p_new_password=>'"""+escaped+"""',
   p_developer_roles=>'ADMIN:CREATE:DATA_LOADER:EDIT:HELP:MONITOR:SQL',
   p_change_password_on_first_use=>'N');
 commit;
end;
/
"""
sql(body,'isolated-verifier-access.log',redactions=(password,escaped))
print('Updated only E5_PAGE / VERIFIER. Sign in with your supplied password; no password file was saved.')
