import sys,unittest,copy
sys.path.insert(0,'scripts')
from candidate_testing import plan,aggregate,POLICY_HASH
class CandidatePolicy(unittest.TestCase):
 def test_selection(self):
  for cadence in ['pr','scheduled','prerelease']:
   self.assertEqual(set(plan(cadence,['migrations.sql','contracts.json'])),{'source','migration','compilation','state','backend'})
  self.assertEqual(len(plan('pr',['unknown.txt'])),5)
  for value in ['bogus','',None]:
   with self.assertRaises(ValueError):plan(value,[])
  with self.assertRaises(ValueError):plan('pr',[],disabled=['backend'])
 def test_aggregation(self):
  required=plan('pr',['migrations.sql']);identity={'merge':'a'*40,'tree':'b'*40,'cadence':'pr','policy':POLICY_HASH}
  good={s:dict(identity,status='success',count=1) for s in required}
  self.assertTrue(aggregate(required,good,identity)['success'])
  for state in ['skipped','neutral','cancelled','failure','disabled','flaky']:
   bad=copy.deepcopy(good);bad['backend']['status']=state
   self.assertFalse(aggregate(required,bad,identity)['success'])
  for count in [0,-1,None,True]:
   bad=copy.deepcopy(good);bad['backend']['count']=count
   self.assertFalse(aggregate(required,bad,identity)['success'])
  for key in identity:
   bad=copy.deepcopy(good);bad['backend'][key]='other'
   self.assertFalse(aggregate(required,bad,identity)['success'])
  for reports in [{},dict(good,backend={})]:self.assertFalse(aggregate(required,reports,identity)['success'])
  for policy in [[],['source'],['unknown']]:
   with self.assertRaises(ValueError):aggregate(policy,good,identity)
  failed=copy.deepcopy(good);failed['migration']['status']='failure';del failed['backend']
  self.assertEqual(aggregate(required,failed,identity)['first_failure'],'migration')
if __name__=='__main__':unittest.main()
