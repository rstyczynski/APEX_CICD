import sys,unittest,io,zipfile
sys.path.insert(0,'scripts')
from release_validation import build,verify
class Integrity(unittest.TestCase):
 def setUp(self):
  self.files={k:b'valid' for k in ['migration.sql','application.sql','configuration.json','contracts.json','evidence.txt']}
  self.archive,self.pin=build(self.files,'a'*40,'1.1.0',{'greeting':'1.1.0'})
 def test_valid(self): self.assertEqual(verify(self.archive,self.pin)['release'],'1.1.0')
 def altered(self,key):
  out=io.BytesIO()
  with zipfile.ZipFile(io.BytesIO(self.archive)) as src,zipfile.ZipFile(out,'w') as dst:
   for n in src.namelist(): dst.writestr(n,b'changed' if n==key else src.read(n))
  with self.assertRaises(ValueError): verify(out.getvalue(),self.pin)
 def test_archive_substitution(self): self.altered('migration.sql')
 def test_report_substitution(self): self.altered('evidence.txt')
 def test_manifest_substitution(self): self.altered('manifest.json')
 def test_missing_evidence(self):
  del self.files['evidence.txt']
  with self.assertRaises(ValueError): build(self.files,'a'*40,'1.1.0',{'greeting':'1.1.0'})
 def test_empty_evidence(self):
  self.files['evidence.txt']=b''
  with self.assertRaises(ValueError): build(self.files,'a'*40,'1.1.0',{'greeting':'1.1.0'})
if __name__=='__main__':unittest.main()
