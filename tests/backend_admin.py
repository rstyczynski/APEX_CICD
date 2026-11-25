"""Fixed prepared-host SQL boundary for the isolated E.5 page fixture."""
from pathlib import Path
import subprocess,re
ROOT=Path(__file__).resolve().parents[1]
def sql(body,name,redactions=()):
 prefix='whenever sqlerror exit failure rollback\nwhenever oserror exit failure rollback\nset define off\nset sqlblanklines on\nset pagesize 0\nset linesize 32767\nset long 10000000\nset longchunksize 32767\nset serveroutput on\nalter session set container=FREEPDB1;\nset serveroutput on\n'
 r=subprocess.run(['podman','--connection','apex-cicd','exec','-i','--user','oracle','apex-db','bash','-lc','sqlplus -s / as sysdba'],input=prefix+body+'\nprompt E5_ADMIN_COMPLETE\nexit\n',text=True,capture_output=True,timeout=180)
 out=r.stdout+r.stderr
 for value in sorted(redactions,key=len,reverse=True):
  if value:out=out.replace(value,"[REDACTED]")
 (ROOT/'progress/E.5/tests'/name).write_text(out)
 if r.returncode or re.search(r'(?m)^\s*(ORA-|PLS-|SP2-)',out) or 'E5_ADMIN_COMPLETE' not in out:raise RuntimeError(out[-2000:])
 return out
