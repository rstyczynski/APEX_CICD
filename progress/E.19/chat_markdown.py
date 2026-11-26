"""Readable conversation views of retained records; raw snapshots remain separate."""
import json,re
from collections import Counter

def content_text(value):
    if isinstance(value,str):return value
    if isinstance(value,list):return '\n\n'.join(filter(None,(content_text(v) for v in value)))
    if isinstance(value,dict):
        if value.get('type') in ('input_text','output_text','text'):return value.get('text','')
        if value.get('type') in ('image','input_image','image_url'):return '[Image attachment; native record retains its reference.]'
        if 'text' in value:return content_text(value['text'])
    return ''

def plain(value,level=0):
    """Unwrap structured tool envelopes into labels and text, never JSON dumps."""
    if isinstance(value,str):
        stripped=value.strip()
        if stripped.startswith(('{','[')):
            try:return plain(json.loads(stripped),level)
            except (ValueError,RecursionError):pass
        lines=value.splitlines()
        if len(lines)>1 and any(l.lstrip().startswith(('{','[')) for l in lines):
            return '\n'.join(plain(l,level) if l.lstrip().startswith(('{','[')) else l for l in lines)
        return value
    if isinstance(value,list):return '\n\n'.join(plain(v,level) for v in value)
    if isinstance(value,dict):
        if str(value.get('type','')).lower()=='reasoning':return '[Internal reasoning omitted]'
        if value.get('type')=='text' and 'text' in value:return plain(value['text'],level)
        if value.get('type') in ('image','image_url','input_image'):return '[Returned image; native snapshot retains available image/reference data.]'
        lines=[]
        for k,v in value.items():
            label=k.replace('_',' ').capitalize()
            body=plain(v,level+1)
            lines.append(f'{label}:\n{body}' if isinstance(v,(dict,list)) or '\n' in body else f'{label}: {body}')
        return '\n\n'.join(lines)
    if value is None:return 'Not provided'
    return str(value)

def fence(text,language='text'):
    longest=max([len(m.group()) for m in re.finditer(r'`{3,}',text)]+[2])
    mark='`'*max(3,longest+1)
    return f'{mark}{language}\n{text.rstrip()}\n{mark}'

def render(records,thread,exported,context,include_tools=True):
    out=['# Sprint E.19 — chat history','',f'**Thread:** `{thread}`  ',f'**Exported:** {exported}  ',f'**Context:** {context}','',
         'User requests and assistant responses appear in conversation order. Tool calls and results are preserved in collapsed activity sections. Structured source records are retained separately; this is a formatted fallback transcript, not a native `/export` result. Internal reasoning/instructions, accounting/state records and duplicate event copies are not conversation turns and are omitted. Explicit privacy redactions remain marked. Native writer lag and messages after this snapshot are outside its coverage.','']
    if not include_tools:
        out[6]='This conversation view contains user requests and assistant responses only. Tool activity is available in the linked full archive. Internal reasoning/instructions and duplicate metadata are omitted. Writer lag and later messages are outside coverage.'
    counts=Counter();calls={}
    # Response records are canonical; event messages are used only if their text is absent there.
    response_texts={(p.get('role'),content_text(p.get('content',[])).strip()) for r in records if r.get('type')=='response_item' and (p:=r.get('payload',{})).get('type')=='message'}
    for n,r in enumerate(records,1):
        p=r.get('payload',{});kind=p.get('type');stamp=r.get('timestamp','');label=None;text=''
        if r.get('type')=='response_item' and kind=='message' and p.get('role') in ('user','assistant'):
            label='User' if p['role']=='user' else 'Assistant';text=content_text(p.get('content',[]))
        elif r.get('type')=='event_msg' and kind=='item_completed':
            item=p.get('item',{});role={'UserMessage':'user','AgentMessage':'assistant'}.get(item.get('type'))
            if role:
                text=content_text(item.get('content',[])) or item.get('text','')
                if (role,text.strip()) not in response_texts:label='User' if role=='user' else 'Assistant'
        if label and text:
            counts[label]+=1;out.extend([f'## {label} · {stamp}', '', text.rstrip(),'']);continue
        if r.get('type')!='response_item':continue
        if not include_tools:continue
        if p.get('redaction'):
            counts['redactions']+=1;out.extend(['> '+p['redaction'],'']);continue
        if kind in ('function_call','custom_tool_call'):
            name=p.get('name','Tool');calls[p.get('call_id')]=name;counts['calls']+=1
            args=p.get('arguments',p.get('input',''))
            body=args if kind=='custom_tool_call' and isinstance(args,str) else plain(args)
            out.extend([f'<details><summary>Tool call: {name} · {stamp}</summary>','',fence(body,'javascript' if kind=='custom_tool_call' else 'text'),'','</details>',''])
        elif kind in ('function_call_output','custom_tool_call_output'):
            name=calls.get(p.get('call_id'),'Tool');counts['results']+=1
            out.extend([f'<details><summary>Tool result: {name} · {stamp}</summary>','',fence(plain(p.get('output',''))),'','</details>',''])
    out.extend(['---','',f'**Coverage:** {len(records)} accessible native records; {counts["User"]} user messages, {counts["Assistant"]} assistant messages, {counts["calls"]} tool calls and {counts["results"]} tool results rendered. {counts["redactions"]} response records carry explicit privacy redactions. Structured files retain record-level metadata and other redacted duplicate events. This file does not claim unavailable or future messages.',''])
    return '\n'.join(line.rstrip() for line in '\n'.join(out).splitlines())+'\n',counts
