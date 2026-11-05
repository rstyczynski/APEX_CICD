import xml.etree.ElementTree as E,json,re,html
r=E.parse('progress/E.3/model.drawio').getroot();d=next(x for x in r.findall('diagram') if x.get('name')=='general lifecycle')
cells=[]
for c in d.findall('.//mxCell'):
 g=c.find('mxGeometry')
 if g is None:continue
 style=dict(x.split('=',1) for x in c.get('style','').split(';') if '=' in x)
 value=c.get('value','');value=re.sub(r'<(?:div|br)[^>]*>','\n',value);value=html.unescape(re.sub('<[^>]+>','',value)).strip()
 cell=dict(c.attrib);cell['value']=value;cell['style']=style;cell['geometry']=dict(g.attrib)
 cell['points']=[dict(x.attrib) for x in g.findall('.//mxPoint')]
 cells.append(cell)
open('.local-apex/e3/presentation-build/model.json','w').write(json.dumps(cells))
