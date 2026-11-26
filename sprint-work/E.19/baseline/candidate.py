import json,re,sys
from pathlib import Path
event=json.loads(Path(sys.argv[1]).read_text())
assert event['state']=='open' and event['base']['ref']=='main'
head,base=event['head']['sha'],event['base']['sha']
assert re.fullmatch('[0-9a-f]{40}',head) and re.fullmatch('[0-9a-f]{40}',base)
