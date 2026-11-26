"""Check local gallery/evidence links and synchronized source disclosures; no UI simulation."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import re
ROOT=Path(__file__).resolve().parents[2];SPRINT=Path(__file__).parent
class Gallery(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set();self.images=[];self.nav=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  if tag=='a' and 'href' in a:self.links.append(a['href'])
  if tag=='img':self.images.append(a['src']);self.links.append(a['src'])
  if tag=='nav':self.nav+=1

def slug(text):
 text=re.sub(r'[^\w\- ]','',text.lower());return text.replace(' ','-')
def resolve(owner,url,ids=None):
 u=urlsplit(url)
 if u.scheme or u.netloc:return
 target=(owner.parent/unquote(u.path)).resolve() if u.path else owner.resolve()
 if not target.exists():raise ValueError(f'broken local link: {owner.relative_to(ROOT)} -> {url}')
 if u.fragment:
  fragment=unquote(u.fragment)
  if target==owner.resolve() and ids is not None:
   if fragment not in ids:raise ValueError('missing gallery navigation target '+url)
  elif target.suffix=='.md':
   anchors={slug(x.lstrip('#').strip()) for x in target.read_text().splitlines() if x.startswith('#')}
   if fragment not in anchors:raise ValueError('missing Markdown anchor '+url)
gallery=SPRINT/'screenshots/index.html';g=Gallery();g.feed(gallery.read_text())
for url in g.links:resolve(gallery,url,g.ids)
if g.nav<5 or len(g.images)<5:raise ValueError('incomplete gallery scenarios')
count=0
for p in [*SPRINT.glob('*.md'),SPRINT/'screenshots/evidence-index.md']:
 text=re.sub(r'```.*?```','',p.read_text(),flags=re.S)
 for url in re.findall(r'\[[^\]]*\]\(([^)]+)\)',text):resolve(p,url);count+=1
walk=(SPRINT/'sprint_E.18_increment_demo.md').read_text();dispatch=walk.index('gh workflow run native.yml')
for name in ['backend-bootstrap.sql','backend-api.sql','backend-tests.sql','application.sql']:
 source='\n'.join(x.rstrip() for x in (ROOT/'sprint-work/E.18'/name).read_text().splitlines()).strip()
 if source not in walk[:dispatch]:raise ValueError('SQL source missing/stale or disclosed after dispatch: '+name)
print(f'PASS {len(g.links)} gallery image/evidence/navigation targets; {count} current-sprint Markdown links; four complete SQL disclosures synchronized before dispatch. Actual rendering/navigation requires the separate browser inspection.')

index=(SPRINT/'screenshots/evidence-index.md').read_text()
for capture in (SPRINT/'screenshots').glob('*.png'):
 if capture.name not in index:raise ValueError('unindexed screenshot '+capture.name)
if walk.index('## Native SQL ledger')>dispatch:raise ValueError('native SQL disclosed after invocation')
print('PASS every PNG indexed; native SQL ledger precedes dispatch.')
