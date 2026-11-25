"""Explicit declaration validation; never infer compatibility from source diffs."""
import json,re
from pathlib import Path
def version(value):
 if not re.fullmatch(r'(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)',value):raise ValueError('Expected explicit major.minor.patch')
 return tuple(map(int,value.split('.')))
def validate(value):
 components=value['components']
 for name,component in components.items():
  version(component['version'])
  for dependency,bounds in component.get('requires',{}).items():
   actual=version(components[dependency]['version'])
   tokens=bounds.split()
   if len(tokens)!=2:raise ValueError('Only explicit >= lower and < upper dependency bounds are supported')
   for token in tokens:
    match=re.fullmatch(r'(>=|<)(\d+\.\d+\.\d+)',token)
    if not match:raise ValueError('Unsupported dependency bound')
    bound=version(match[2]);valid=actual>=bound if match[1]=='>=' else actual<bound
    if not valid:raise ValueError(name+' rejects '+dependency+' '+str(actual)+' against '+bounds)
 return {k:v['version'] for k,v in components.items()}
def qualified_toolchain(project_version,actual):
 if project_version!='25.4.1.0' or 'Release '+project_version+' Production Build: 25.4.1.022.0618' not in actual:
  raise ValueError('Source SQLcl release or qualified build mismatch; stop before native mutation')
 return True
if __name__=='__main__':
 root=Path(__file__).resolve().parents[1]
 print(validate(json.loads((root/'examples/secure-backend/contracts.json').read_text())))
