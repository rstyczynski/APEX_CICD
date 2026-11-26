"""Verify local artifact links and exact SQL disclosures; UI rendering is separate."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import re
ROOT=Path(__file__).resolve().parents[2];S=Path(__file__).parent
class Gallery(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set()
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  if tag=='a' and 'href' in a:self.links.append(a['href'])
  if tag=='img':self.links.append(a['src'])
def resolve(owner,url,ids=None):
 u=urlsplit(url)
 if u.scheme or u.netloc:return
 target=(owner.parent/unquote(u.path)).resolve() if u.path else owner.resolve()
 if not target.exists():raise RuntimeError(f'broken local link {owner}: {url}')
 if u.fragment and target==owner.resolve() and ids is not None and u.fragment not in ids:raise RuntimeError('broken navigation '+url)
g=S/'screenshots/index.html';parser=Gallery();parser.feed(g.read_text())
for link in parser.links:resolve(g,link,parser.ids)
count=0
for p in [*S.glob('*.md'),S/'screenshots/evidence-index.md',S/'chat/index.md']:
 text=re.sub(r'```.*?```','',p.read_text(),flags=re.S)
 for url in re.findall(r'\[[^\]]*\]\(([^)]+)\)',text):resolve(p,url);count+=1
walk=(S/'sprint_E.19_increment_demo.md').read_text();dispatch=walk.index('gh workflow run acceptance.yml')
for name in ['backend-bootstrap.sql','backend-api.sql','backend-tests.sql','application.sql']:
 source=(ROOT/'sprint-work/E.19'/name).read_text().rstrip()
 if source not in walk[:dispatch]:raise RuntimeError('missing complete SQL disclosure '+name)
index=(S/'screenshots/evidence-index.md').read_text()
for p in (S/'screenshots').glob('*.png'):
 if p.name not in index:raise RuntimeError('unindexed capture '+p.name)
print(f'PASS {len(parser.links)} gallery targets and {count} current-document links; complete SQL disclosures; every capture indexed. UI rendering/nav and slide inspection are separate observations.')
