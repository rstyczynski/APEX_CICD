#!/usr/bin/env python3
"""Read-only ownership boundary check before named lab destruction."""
import json, subprocess

def p(*args):
    return json.loads(subprocess.check_output(['podman','--connection','apex-cicd',*args],text=True))
owned={'apex-db','apex-ords'}
volumes={'apex-data','apex-ords-config','apex-images'}
def check(rows, details):
    for row in rows:
        name=row['Names'][0]
        detail=details[row['Id']]
        mounts=detail.get('Mounts',[])
        touched={m.get('Name') for m in mounts}&volumes
        networks=set(detail.get('NetworkSettings',{}).get('Networks',{}))
        if name not in owned:
            secrets=detail.get('Config',{}).get('Secrets',[])
            shared_secret=any(x.get('Name')=='apex-db-password' for x in secrets)
            if touched or 'apex-net' in networks or shared_secret:
                raise SystemExit('REFUSED: unrelated container shares lab resources: '+name)
            continue
        expected={'apex-db':{'apex-data','apex-images'},'apex-ords':{'apex-ords-config','apex-images'}}[name]
        if {m.get('Name') for m in mounts} != expected or networks != {'apex-net'}:
            raise SystemExit('REFUSED: unexpected mount/network inventory for '+name)
        image=detail.get('ImageName','')
        if name=='apex-db' and not image.startswith(('docker.io/gvenzl/oracle-free:','docker.io/gvenzl/oracle-free@')):
            raise SystemExit('REFUSED: unexpected database image')
        if name=='apex-ords' and not image.startswith('container-registry.oracle.com/database/ords@'):
            raise SystemExit('REFUSED: unexpected ORDS image')
        print('OWNED '+name+': expected named volumes and apex-net; '+image)

if __name__=='__main__':
    rows=p('ps','-a','--format','json')
    check(rows,{r['Id']:p('inspect',r['Id'])[0] for r in rows})
    print('PASS ownership boundary: no unrelated container consumes owned volumes/network/secret.')
