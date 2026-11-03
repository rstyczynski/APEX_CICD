test_SM1_pipeline_contract() {
  actionlint -config-file examples/git-pipeline/.github/actionlint.yaml examples/git-pipeline/.github/workflows/*.yml
  python3 - <<'PY'
import importlib.util
from pathlib import Path
import subprocess
import yaml
p=Path('examples/git-pipeline/scripts/check_pr.py')
spec=importlib.util.spec_from_file_location('classify',p);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
for label,title in [('patch','fix: update Home heading'),('minor','feat: add greeting'),('major','feat!: replace contract'),('patch','fix(home): title')]:
    assert mod.classify({'labels':[{'name':label}],'title':title})==label
for labels,title in [([], 'fix: title'),(['patch','minor'],'fix: title'),(['patch'],'feat: title'),(['major'],'feat: title'),(['minor'],'feat!: title')]:
    try: mod.classify({'labels':[{'name':x} for x in labels],'title':title})
    except ValueError: pass
    else: raise AssertionError((labels,title))
directory=Path('examples/git-pipeline/.github/workflows')
workflows={p.stem:yaml.load(p.read_text(),Loader=yaml.BaseLoader) for p in directory.glob('*.yml')}
assert set(workflows['release']['on'])=={'workflow_dispatch'}
assert 'pull_request' in workflows['pr']['on'] and 'push' in workflows['version']['on']
assert 'version_tag' in workflows['release']['on']['workflow_dispatch']['inputs']
for name in ['pr','version']:
    assert all(j['runs-on']=='ubuntu-latest' for j in workflows[name]['jobs'].values())
    assert 'E3_LAB_CONFIG' not in (directory/(name+'.yml')).read_text()
for script in Path('examples/git-pipeline/scripts').glob('*.sh'):
    subprocess.run(['bash','-n',str(script)],check=True)
print('PASS workflow boundaries and 9 PR classification cases')
PY
}
