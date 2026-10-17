#!/usr/bin/env python3
"""Explicit contract rules for the two supported prototype combinations."""
import json,sys

def validate(m):
    components=m['components']
    for dependent in ('Hello','World'):
        required=m['dependencies'][dependent]['Foundation']
        if required!=components['Foundation']:
            raise ValueError(f'{dependent} requires Foundation {required}; proposed Foundation {components["Foundation"]}')
    if components not in ({'Foundation':'1.0.0','Hello':'1.0.0','World':'1.0.0'},
                          {'Foundation':'1.0.0','Hello':'1.0.1','World':'1.0.0'}):
        raise ValueError('Component triple is not explicitly supported by this prototype')

if __name__=='__main__':
    try:
        if len(sys.argv)!=2: raise ValueError('Usage: cicd-compatibility.py MANIFEST')
        validate(json.load(open(sys.argv[1])))
        print('PASS explicit component dependencies and supported version triple')
    except (ValueError,KeyError,OSError) as exc:
        sys.exit('REJECTED INCOMPATIBLE: '+str(exc))
