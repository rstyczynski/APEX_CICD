"""Reject native errors even when SQLcl returns zero."""
import re,sys
from pathlib import Path
text=re.sub(r'\x1b\[[0-9;]*m','',Path(sys.argv[1]).read_text())
if re.search(r'Errors:\s*[1-9]|(?im:^\s*(?:ORA-|PLS-|SP2-|ERROR\b|Error starting|Unknown Command))|Expected a subcommand',text):
    raise SystemExit('native output contains errors')
