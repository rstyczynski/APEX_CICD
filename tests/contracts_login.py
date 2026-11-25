"""Set the existing isolated ALICE password through native APEX API."""
import getpass,sys
from contracts_lab import execute as sql
if sys.argv[1:]==['--password-stdin']:
 password=sys.stdin.readline().rstrip('\r\n')
elif not sys.argv[1:]:
 password=getpass.getpass('New password for E6_APP / ALICE: ')
else:raise SystemExit('Usage: contracts_login.py [--password-stdin]')
if len(password)<16 or '\n' in password or '\r' in password:raise SystemExit('Use at least 16 characters and no line breaks.')
escaped=password.replace("'","''")
body="""begin
 apex_util.set_security_group_id(apex_util.find_security_group_id('E6_APP'));
 apex_util.edit_user(
   p_user_id=>apex_util.get_user_id('ALICE'),
   p_user_name=>'ALICE',
   p_web_password=>'"""+escaped+"""',
   p_new_password=>'"""+escaped+"""',
   p_change_password_on_first_use=>'N');
 commit;
end;
/
"""
sql(body,'isolated-alice-access.log',redactions=(password,escaped))
print('Updated only E6_APP / ALICE. Sign in with your supplied password; no password file was saved.')
