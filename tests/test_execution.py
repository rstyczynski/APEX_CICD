import sys, unittest, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from isolated_execution import Registry, bounded, review
import json
class Execution(unittest.TestCase):
 def test_streams(self):
  r=Registry(); a,_=r.admit('pr-a','1','event'); b,_=r.admit('pr-b','1','event'); rel,_=r.admit('release','1','event')
  self.assertEqual(r.admit('pr-a','1','event'),(a,None))
  newer,old=r.admit('pr-a','2','event2'); self.assertEqual(old,a)
  with self.assertRaises(ValueError):r.complete('pr-a',a,'success')
  r.complete('pr-b',b,'success');r.complete('release',rel,'success');r.complete('pr-a',newer,'failure')
  retry,old=r.admit('pr-a','2','explicit-retry');self.assertNotEqual(retry,newer)
  r.complete('pr-a',retry,'success')
  with self.assertRaises(ValueError):r.complete('pr-a',retry,'success')
 def test_retries(self):
  calls=[]
  def transient():
   calls.append(1);raise TimeoutError('unavailable')
  with self.assertRaises(TimeoutError):bounded(transient)
  self.assertEqual(len(calls),3); calls.clear()
  def assertion():
   calls.append(1);raise AssertionError('mandatory failure')
  with self.assertRaises(AssertionError):bounded(assertion)
  self.assertEqual(len(calls),1)
 def test_inert(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'injected';text=f'$(touch {p}); `touch {p}`'
   self.assertEqual(json.loads(review(text))['review'],text);self.assertFalse(p.exists())
unittest.main()
