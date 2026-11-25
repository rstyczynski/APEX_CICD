"""Real disposable Git journey; no remote writes and no hosted enforcement claim."""
import importlib.util,json,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('review',ROOT/'scripts/review_control.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
out=ROOT/'progress/E.9/tests';out.mkdir(exist_ok=True)
def git(path,*args):return subprocess.check_output(['git','-C',str(path),*args],text=True,stderr=subprocess.STDOUT).strip()
with tempfile.TemporaryDirectory(prefix='e9-review-') as tmp:
 repo=Path(tmp)/'source';repo.mkdir();git(repo,'init','-b','main');git(repo,'config','user.name','E9 Lab');git(repo,'config','user.email','e9@example.invalid')
 f=repo/'greeting.py';f.write_text('def greet(name):\n    return "Hello " + name\n');git(repo,'add','.');git(repo,'commit','-m','base');base=git(repo,'rev-parse','HEAD')
 git(repo,'checkout','-b','feature');f.write_text('def greet(name):\n    return "Hello " + name.strip()\n');git(repo,'commit','-am','Trim greeting input');head=git(repo,'rev-parse','HEAD')
 initial=git(repo,'diff',base,head);(out/'initial.diff').write_text(initial)
 annotation='Developer: keep the Hello prefix; whitespace normalization only.'
 (out/'summary-initial.md').write_text('Trim outer whitespace in greeting input.\n\n'+annotation+'\nTests: not run. Limitation: blank names remain allowed.\n')
 # Refresh the actual diff after scope changes.
 (repo/'test_greeting.py').write_text('from greeting import greet\nassert greet(" World ")=="Hello World"\n')
 git(repo,'add','.');git(repo,'commit','-m','Add greeting regression assertion');head=git(repo,'rev-parse','HEAD')
 diff=git(repo,'diff',base,head);(out/'refreshed.diff').write_text(diff)
 subprocess.run(['python3','test_greeting.py'],cwd=repo,check=True)
 (out/'summary-refreshed.md').write_text('Trim outer whitespace and add one Python assertion.\n\n'+annotation+'\nTests: python3 test_greeting.py PASS.\nCorrection: “all security tests passed” is unsupported and removed.\nLimitations: blank-name handling and non-string inputs are unchanged; no security suite ran.\n')
 # Report authored by the actual Codex reviewer after inspecting retained diff.
 template=json.loads((out/'agent-review-template.json').read_text())
 report={**template,'base':base,'head':head,'policy':m.digest({'assessments':m.ASSESSMENTS,'independent_approval':True})}
 accepted=m.receipt(report,'developer');candidate=accepted['candidate']
 store=out/'reports';store.mkdir(exist_ok=True);saved=store/(accepted['report']+'.json');saved.write_text(json.dumps(report,indent=2)+'\n');assert m.digest(json.loads(saved.read_text()))==accepted['report']
 checks={n:{'publisher':n.lower()+'-controller','state':'success','candidate':candidate} for n in ('Testing','Review')}
 args=dict(candidate=candidate,receipt=accepted,report=report,checks=checks,writer='integrator',conversations=0,approved=True)
 assert m.publish(accepted,candidate,report,lambda:candidate)
 assert not m.publish(accepted,candidate,report,lambda:{**candidate,'head':'raced'})
 decision=m.authorize(**args);assert decision['allowed'];git(repo,'checkout','main');assert git(repo,'rev-parse','HEAD')==base
 git(repo,'merge','--no-ff','feature','-m','Controlled local integration');subprocess.run(['python3','test_greeting.py'],cwd=repo,check=True)
 git(repo,'bundle','create',str(out/'candidate.bundle'),'--all')
 result={'candidate':candidate,'receipt':accepted,'decision':decision,'merge':git(repo,'rev-parse','HEAD'),'diff':diff,'scope':'local trusted controller; no GitHub enforcement','assertion':'PASS'}
 (out/'journey.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
