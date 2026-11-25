import copy, importlib.util, unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('review',Path(__file__).resolve().parents[1]/'scripts/review_control.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class ReviewTests(unittest.TestCase):
 def setUp(self):
  self.r={'base':'b','head':'h','policy':'p','assessments':{k:'inspected; no blocker' for k in m.ASSESSMENTS},'findings':[]}
 def test_policy(self):
  m.validate(self.r,'developer')
  for mutation in ['missing','severity','blocker','ack','submitter']:
   r=copy.deepcopy(self.r);who='developer'
   if mutation=='missing': del r['assessments']['security']
   if mutation=='severity': r['findings']=[{'severity':'surprise'}]
   if mutation=='blocker': r['findings']=[{'severity':'blocker','state':'open'}]
   if mutation=='ack': r['findings']=[{'severity':'blocker','state':'dismissed','reason':'ack'}]
   if mutation=='submitter': who='intruder'
   with self.assertRaises(ValueError,msg=mutation): m.validate(r,who)
 def test_freshness(self):
  receipt=m.receipt(self.r,'developer');live=copy.deepcopy(self.r)
  self.assertTrue(m.current(receipt,live,self.r))
  for field in ['base','head','policy']:
   changed=copy.deepcopy(live);changed[field]+='changed'
   self.assertFalse(m.current(receipt,changed,self.r))
  edited=copy.deepcopy(self.r);edited['assessments']['security']='edited'
  self.assertFalse(m.current(receipt,live,edited))
  self.assertFalse(m.current(receipt,live,None))
  live['withdrawn']=True;self.assertFalse(m.current(receipt,live,self.r))
  self.assertFalse(m.publish(receipt,self.r,self.r,lambda:{**self.r,'head':'raced'}))
 def test_merge(self):
  c={'base':'b','head':'h','policy':'p'};r=m.receipt(self.r,'developer')
  checks={name:{'publisher':name.lower()+'-controller','state':'success','candidate':c} for name in ['Testing','Review']}
  args=dict(candidate=c,receipt=r,report=self.r,checks=checks,writer='integrator',conversations=0,approved=True)
  self.assertTrue(m.authorize(**args)['allowed'])
  for name in checks:
   for field,value in [('publisher','impostor'),('state','neutral'),('state','failure'),('state','cancelled'),('candidate',{})]:
    bad=copy.deepcopy(args);bad['checks'][name][field]=value
    self.assertFalse(m.authorize(**bad)['allowed'])
   bad=copy.deepcopy(args);del bad['checks'][name];self.assertFalse(m.authorize(**bad)['allowed'])
  for field,value in [('conversations',1),('writer','developer'),('approved',False),('report',None)]:
   bad=copy.deepcopy(args);bad[field]=value;self.assertFalse(m.authorize(**bad)['allowed'])
  bad=copy.deepcopy(args);bad['conversations']=1;bad['bypass']='emergency-123';bad['writer']='administrator'
  self.assertEqual(m.authorize(**bad)['bypass'],'emergency-123')
if __name__=='__main__':unittest.main()
