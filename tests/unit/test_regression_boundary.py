"""Private regression routing tests; no database access or retained credentials."""
import json,os,subprocess,sys,tempfile,unittest,importlib.util
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
import apex_sql as sql

class PrivateRegressionRouting(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory(prefix='e12-boundary-');self.addCleanup(self.temp.cleanup)
  self.state=Path(self.temp.name);self.secret='E12_synthetic_private_marker'
  (self.state/'credentials.env').write_text('ORACLE_PASSWORD='+self.secret+'\n')
  (self.state/'e1-secrets.json').write_text(json.dumps({'E1_CTRL':self.secret}))
  self.profile=self.state/'profiles';self.profile.mkdir()
  self.config=sql.ROOT/'config/areas.json';self.original=self.config.read_bytes()
  self.addCleanup(lambda:self.assertEqual(self.config.read_bytes(),self.original))
  self.local=patch.object(sql,'LOCAL',self.state);self.local.start();self.addCleanup(self.local.stop)
  self.env=patch.dict(os.environ,{'APEX_CICD_CONNECTIONS':str(self.profile),'APEX_CICD_SERVICE':'127.0.0.1:1521/E12REG','APEX_CICD_ADMIN_USER':'E12_ADMIN'},clear=False)
  self.env.start();self.addCleanup(self.env.stop)
 def invoke(self,admin=True,fail=False,connection=None):
  seen={}
  def child(args,**kw):
   seen.update(args=args,**kw)
   assert (self.state/'run-sql').exists()
   assert len(list((self.state/'run-sql').glob('*.sql')))==1
   return subprocess.CompletedProcess(args,1 if fail else 0,'ORA-20001: '+self.secret if fail else 'E1_SQL_COMPLETE\n','')
  with patch.object(sql.subprocess,'run',side_effect=child):
   if fail:
    with self.assertRaises(RuntimeError) as caught:sql.run('select 1 from dual;',admin=admin,connection=connection)
    self.assertNotIn(self.secret,str(caught.exception));self.assertIn('[REDACTED]',str(caught.exception))
   else:sql.run('select 1 from dual;',admin=admin,connection=connection)
  self.assertEqual(list((self.state/'run-sql').glob('*.sql')),[])
  return seen
 def test_private_context_and_cleanup(self):
  seen=self.invoke();self.assertIn('E12_ADMIN/',seen['input']);self.assertIn('@//127.0.0.1:1521/E12REG',seen['input'])
  self.assertNotIn('as sysdba',seen['input']);self.assertNotIn(self.secret,' '.join(seen['args']))
  self.assertEqual(seen['args'][seen['args'].index('-home')+1],str(self.profile))
 def test_original_sys_authentication_preserved(self):
  with patch.dict(os.environ,{'APEX_CICD_ADMIN_USER':'SYS'}):seen=self.invoke()
  self.assertIn('as sysdba',seen['input'])
 def test_failure_redaction_and_cleanup(self):self.invoke(fail=True)
 def test_invalid_admin_rejected_before_child(self):
  with patch.dict(os.environ,{'APEX_CICD_ADMIN_USER':'E12_ADMIN;unsafe'}),patch.object(sql.subprocess,'run') as child:
   with self.assertRaisesRegex(ValueError,'Invalid admin identity'):sql.run('select 1 from dual;',admin=True)
   child.assert_not_called()
 def test_credentials_come_from_explicit_private_state(self):self.assertEqual(sql.secrets()['E1_CTRL'],self.secret)
 def test_default_author_uses_ephemeral_home_and_read_only_record(self):
  (self.state/'e1-secrets.json').write_text(json.dumps({'E1_DEV_C':self.secret}))
  with patch.object(sql,'TOOLS',self.state):
   os.environ.pop('APEX_CICD_CONNECTIONS',None)
   self.assertNotIn('ORACLE_PASSWORD',sql.secrets())
   seen=self.invoke(admin=False,connection='lab-dev-c')
  self.assertIn('connect E1_DEV_C/',seen['input']);self.assertNotIn('connect -name',seen['input'])
  home=Path(seen['args'][seen['args'].index('-home')+1])
  self.assertFalse(home.exists());self.assertNotEqual(home,self.profile)
 def test_checkout_profile_is_rejected(self):
  with patch.dict(os.environ,{'APEX_CICD_CONNECTIONS':str(sql.ROOT/'.local-apex/tools/sqlcl-home')}),patch.object(sql.subprocess,'run') as child:
   with self.assertRaisesRegex(ValueError,'profiles must be outside'):sql.run('select 1 from dual;',connection='lab-dev-c')
   child.assert_not_called()
 def test_default_administrative_source_is_rejected(self):
  with patch.object(sql,'TOOLS',self.state),patch.object(sql.subprocess,'run') as child:
   with self.assertRaisesRegex(ValueError,'explicit private inputs'):sql.run('select 1 from dual;',admin=True)
   child.assert_not_called()


 def test_platform_cannot_rewrite_default_scratch_record(self):
  spec=importlib.util.spec_from_file_location('e12_platform_guard',sql.ROOT/'scripts/cicd-platform.py')
  platform=importlib.util.module_from_spec(spec);spec.loader.exec_module(platform)
  with patch.object(platform,'ROOT',self.state),patch.object(platform,'LOCAL',self.state/'.local-apex'):
   with self.assertRaisesRegex(ValueError,'outside the checkout'):platform.credentials(['E1_DEV_C'])
   with self.assertRaisesRegex(ValueError,'outside the checkout'):platform.owned_inventory()
   self.assertFalse((self.state/'.local-apex').exists())

if __name__=='__main__':unittest.main()
